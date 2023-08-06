import hashlib

from sklearn.utils._param_validation import (Integral, Interval, StrOptions,
                                             validate_params)

from pec.utils.seed import RandomStateGenerator

from ..clustering.algo.kmeans import MonolithicKMeansRun
from ..decision.inertia_based import InertiaBased_MonolithicDecisionWorker


class MonolithicEnsembleClustering:
    """Monolithic Ensemble Clustering

    ----------
    parameters :

        data : array-like or sparse matrix.

        n_clusters : number of clusters >= 2.

        n_runs : number of (monolithic) runs to execute >= 1.

        alg : algorithm to use, string in {'k-means', 'k-means++'}.

        decision : decision to use, string in {'inertia', 'hgpa', 'mcla'}.

        random_state : seed for random generator.
    """

    @validate_params(
        {
            'data': ['array-like', 'sparse matrix'],
            'n_clusters': [Interval(Integral, 2, None, closed='left')],
            'n_runs': [Interval(Integral, 1, None, closed='left')],
            'algo': [StrOptions({'k-means', 'k-means++'})],
            'decision': [StrOptions({'inertia', 'hgpa', 'mcla'})],
            "random_state": ['random_state', None],
        }
    )
    def __init__(self, data, n_clusters=2, n_runs=1, alg='k-means', decision='inertia', random_state=None, id=None, verbose=False, instance_name=None):

        self.id = id if id is not None else self.__get_id(data, n_clusters, n_runs, alg, decision, random_state)
        self.data = data
        self.n_entries = data.shape[0]
        self.n_clusters = n_clusters
        self.n_runs = n_runs
        self.alg = alg
        self.decision = decision
        self.instance_name = instance_name if instance_name is not None else self.__get_instance_name()
        self.random_state = random_state
        self.verbose = verbose

        self.__random_state_arr = RandomStateGenerator(self.random_state).get(self.n_runs)

        self.__clustering_run_arr = None
        self__results = []

    def __get_id(self, data, n_clusters, n_runs, alg, decision, random_state):
        """Generates a unique id of this pec instance"""
        rawString = "||||".join([
            str(hashlib.sha256(data.tobytes()).hexdigest()),
            str(n_clusters),
            str(n_runs),
            str(alg),
            str(decision),
            str(random_state)
        ])
        return str(hashlib.sha256(rawString.encode()).hexdigest())

    def __get_instance_name(self):
        if self.alg == "k-means" and self.decision == "inertia":
            return 'I-PecK'
        elif self.alg == "k-means++" and self.decision == "inertia":
            return 'I-PecK++'
        elif self.alg == "k-means" and self.decision == "hgpa":
            return 'HGPA-PecK'
        elif self.alg == "k-means++" and self.decision == "hgpa":
            return 'HGPA-PecK++'
        elif self.alg == "k-means" and self.decision == "mcla":
            return 'MCLA-PecK'
        elif self.alg == "k-means++" and self.decision == "mcla":
            return 'MCLA-PecK++'
        else:
            raise RuntimeError(f"Not yet implemented alg-decision pair: '{self.alg} -- {self.decision}'.")

    def __new_arr_MonolithicKMeansRun(self, alg, **kwargs):
        arr = []
        for i in range(self.n_runs):
            kr = MonolithicKMeansRun(self.data, self.n_clusters, alg=alg, random_state=self.__random_state_arr[i],
                                     verbose=self.verbose, **kwargs)
            arr.append(kr)
        return arr

    def __new_InertiaBased_MonolithicDecisionWorker(self):
        return InertiaBased_MonolithicDecisionWorker(self.data, self.n_clusters, verbose=self.verbose)

    def start(self):
        self.__active = True
        result = self.__exec()
        return result

    def __exec(self):
        ###
        ### instantiate workers
        ###
        if self.alg == "k-means" and self.decision == "inertia":
            self.__decision_worker = self.__new_InertiaBased_MonolithicDecisionWorker()
            self.__clustering_run_arr = self.__new_arr_MonolithicKMeansRun(self.alg)
        elif self.alg == "k-means++" and self.decision == "inertia":
            self.__decision_worker = self.__new_InertiaBased_MonolithicDecisionWorker()
            self.__clustering_run_arr = self.__new_arr_MonolithicKMeansRun(self.alg)
        else:
            raise RuntimeError(f"Not yet implemented alg-decision pair: '{self.alg} -- {self.decision}'.")

        ###
        ### start
        ###
        for kr in self.__clustering_run_arr:
            single_result = kr.run()
            self.__decision_worker.addMonolithicResult(single_result)

        final_result = self.__decision_worker.getFinalResult()
        if self.verbose: print(f"[{self.__class__.__name__}] terminated.")
        return final_result
