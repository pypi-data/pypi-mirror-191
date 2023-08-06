import os
import time
from multiprocessing import Process

from ...utils.labels import best_labels_dtype
from ..events import Ack, IterationResultEvent
from .sklearn_cluster_kmeans import KMeans
from ...ensemble.results import MonolithicResult, MonolithicResultInfo, MonolithicResultMetrics
from pec.utils.metrics import ClusteringMetrics

class MonolithicKMeansRun:
    """Monolithic KMeans Run, no partial results, only a final result"""
    def __init__(self, data, n_clusters, random_state=None, alg="k-means", max_iter=299, tol=1e-4, verbose=False, **kwargs):
        self.data = data
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.alg = alg
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.labels_dtype = best_labels_dtype(self.n_clusters)

        self.iteration_count = 0
    
    def run(self):
        
        # partial results fn
        def fn(r):
            self.iteration_count +=1

        t0 = time.time()
        kmean = None
        if self.alg == "k-means":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="random",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(self.data, on_partial_result=fn)
        elif self.alg == "k-means++":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="k-means++",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(self.data, on_partial_result=fn)
        else:
            raise RuntimeError(f"[{self.__class__.__name__} #{self.id}] Undefined alg type '{self.alg}'.")
        
        labels = kmeans.labels_.astype(self.labels_dtype)
        
        t1 = time.time()
        info = MonolithicResultInfo(iteration=self.iteration_count, n_clusters=self.n_clusters, clustering_time=t1-t0)
        metrics = MonolithicResultMetrics(
            inertia=ClusteringMetrics.inertia(self.data, labels)
        )
        result = MonolithicResult(info, metrics, labels)
        return result



class ProgressiveKMeansRun(Process):
    """ Progressive KMeans Clustering Run """

    def __init__(self, id, shared_data, shared_partitions, n_clusters, results_queue, ack_queue, lock,
                 random_state=None, alg="k-means", max_iter=299, tol=1e-4, verbose=False, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.shared_data = shared_data
        self.shared_partitions = shared_partitions
        self.n_clusters = n_clusters

        self.results_queue = results_queue
        self.ack_queue = ack_queue
        self.lock = lock

        self.random_state = random_state
        self.alg = alg
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.labels_dtype = best_labels_dtype(self.n_clusters)

    def run(self):
        if self.verbose: print(f"[{self.__class__.__name__}#{self.id}] started with pid={os.getpid()}.")
        shm_data, data = self.shared_data.open()
        shm_partitions, partitions = self.shared_partitions.open()

        # partial results fn
        def fn(r):
            labels = r.labels.astype(self.labels_dtype)

            partitions[self.id, :] = labels
            it_event = IterationResultEvent(
                timestamp=time.time(),
                run_id=self.id,
                iteration=r.iteration,
                is_last=r.is_last
            )
            self.results_queue.put(it_event)
            if not r.is_last:
                recv_ack = self.ack_queue.get()
                if not isinstance(recv_ack, Ack): raise RuntimeError(
                    f"[{self.__class__.__name__}] Expected an AckEvent, got {recv_ack.__class__.__name__}.")

        ####
        if self.alg == "k-means":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="random",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(data, on_partial_result=fn)
        elif self.alg == "k-means++":
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=1, max_iter=self.max_iter, init="k-means++",
                            random_state=self.random_state, tol=self.tol, algorithm='elkan')
            kmeans.fit(data, on_partial_result=fn)
        else:
            raise RuntimeError(f"[{self.__class__.__name__} #{self.id}] Undefined alg type '{self.alg}'.")

        shm_data.close()
        shm_partitions.close()
        if self.verbose: print(f"[{self.__class__.__name__} #{self.id}] terminated.")
