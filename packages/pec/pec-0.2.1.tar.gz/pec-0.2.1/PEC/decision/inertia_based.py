import os
import time
from multiprocessing import Process

import numpy as np

from ..clustering.events import Ack, IterationResultEvent
from pec.utils.metrics import ClusteringMetrics
from ..ensemble.results import (PartialResult, PartialResultInfo,
                                PartialResultMetrics)
from ..utils.labels import adjustLabels, adjustPartitions


class InertiaBased_EarlyTermination:
    """Methods for computing early termination.
    prev_result is none if curr_result is the first result"""

    @staticmethod
    def slow(prev_result, curr_result):
        if curr_result.info.iteration < 5:
            return False
        target = 10 ** (-5)
        if np.abs(curr_result.metrics.inertia - prev_result.metrics.inertia) <= target:
            return True
        return False

    @staticmethod
    def fast(prev_result, curr_result):
        if curr_result.info.iteration < 5:
            return False
        target = 10 ** (-4)
        if np.abs(curr_result.metrics.inertia - prev_result.metrics.inertia) <= target:
            return True
        return False


class InertiaBased_ProgressiveDecisionWorker(Process):
    """ Inertia Based Progressive Decision Worker """

    def __init__(self, pec_id, shared_data, shared_partitions, n_clusters,
                 partial_results_queue, run_results_queue_arr, run_ack_queue_arr, run_lock_arr,
                 start_time=None, verbose=False, **kwargs):

        super().__init__(**kwargs)

        self.pec_id = pec_id
        self.shared_data = shared_data
        self.shared_partitions = shared_partitions
        self.n_clusters = n_clusters

        self.partial_results_queue = partial_results_queue
        self.run_results_queue_arr = run_results_queue_arr
        self.run_ack_queue_arr = run_ack_queue_arr
        self.run_lock_arr = run_lock_arr

        self.n_runs = len(run_results_queue_arr)
        self.start_time = start_time if start_time is not None else time.time()
        self.verbose = verbose
        self.progressive_iteration = 0

    def run(self):
        if self.verbose: print(f"[{self.__class__.__name__}] started with pid={os.getpid()}.")
        shm_data, data = self.shared_data.open()
        shm_partitions, partitions = self.shared_partitions.open()
        fn_inertia = lambda labels, data: ClusteringMetrics.inertia(data, labels)

        old_result_labels = None
        runs_completed = np.array([False for _ in range(self.n_runs)])
        runs_iterations = np.array([-1 for _ in range(self.n_runs)], dtype=int)

        while not np.all(runs_completed):
            ## get one result from each run
            timestamp_before_clustering_results = time.time()
            for i in range(self.n_runs):
                if runs_completed[i]: continue
                event = self.run_results_queue_arr[i].get()
                if isinstance(event, IterationResultEvent):
                    runs_completed[i] = event.is_last
                    runs_iterations[i] = event.iteration + 1
                else:
                    raise RuntimeError(
                        f"[{self.__class__.__name__}] Expected an IterationResultEvent, got {event.__class__.__name__}")
            timestamp_after_clustering_results = time.time()

            ## compute decision
            timestamp_before_decision = time.time()
            runs_inertia = np.apply_along_axis(fn_inertia, 1, partitions, data),
            best_run = np.argmin(runs_inertia)
            best_inertia = np.min(runs_inertia)
            best_labels = adjustLabels(partitions[best_run, :], old_result_labels)
            adjusted_partitions = adjustPartitions(partitions, best_labels)

            timestamp_after_decision = time.time()
            ## decision computed

            ## send result event
            result_timestamp = time.time() - self.start_time
            result_info = PartialResultInfo(
                pec_id=self.pec_id,
                timestamp=result_timestamp,
                iteration=self.progressive_iteration,
                is_last=np.all(runs_completed),
                n_clusters=self.n_clusters,
                n_runs=self.n_runs,

                best_run=best_run,
                completed_runs=len(np.argwhere(runs_completed == True).flatten()),
                runs_iterations=runs_iterations.tolist(),
                completed_runs_status=runs_completed.tolist(),

                clustering_time=timestamp_after_clustering_results - timestamp_before_clustering_results,
                decision_time=timestamp_after_decision - timestamp_before_decision,
            )

            result_metrics = PartialResultMetrics(
                inertia=best_inertia
            )

            result_labels = best_labels
            old_result_labels = result_labels
            progressive_result = PartialResult(result_info, result_metrics, result_labels, adjusted_partitions)

            self.partial_results_queue.put(progressive_result)
            self.progressive_iteration += 1

            for i in range(self.n_runs):
                if not runs_completed[i]:
                    self.run_ack_queue_arr[i].put(Ack())

        shm_data.close()
        shm_partitions.close()
        if self.verbose: print(f"[{self.__class__.__name__}] terminated.")


class InertiaBased_MonolithicDecisionWorker:
    """ Inertia Based Monolithic Decision Worker """

    def __init__(self, data, n_clusters, start_time=None, verbose=False, **kwargs):
        super().__init__(**kwargs)

        self.data = data
        self.n_clusters = n_clusters
        self.verbose = verbose

        self.bestResult = None
        self.inertia_arr = []

    def addMonolithicResult(self, r):
        self.inertia_arr.append(r.metrics.inertia)
        if self.bestResult is None:
            self.bestResult = r
        else:
            if r.metrics.inertia <= self.bestResult.metrics.inertia:
                self.bestResult = r

    def getFinalResult(self):
        return self.bestResult
