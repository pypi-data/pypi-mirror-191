from .mec import MonolithicEnsembleClustering

class I_MecK(MonolithicEnsembleClustering):
    """ Inertia Based Monolithic Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="inertia", random_state=random_state, id=id, verbose=verbose)


class I_MecKPP(MonolithicEnsembleClustering):
    """ Inertia Based Monolithic Ensemble Kmeans++ """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="inertia", random_state=random_state, id=id, verbose=verbose)
