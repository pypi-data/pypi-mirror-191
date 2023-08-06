from .pec import ProgressiveEnsembleClustering


class I_PecK(ProgressiveEnsembleClustering):
    """ Inertia Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 on_partial_result_callback=None, early_terminator=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="inertia", random_state=random_state, id=id,
                         on_partial_result_callback=on_partial_result_callback, early_terminator=early_terminator, verbose=verbose)


class I_PecKPP(ProgressiveEnsembleClustering):
    """ Inertia Based Progressive Ensemble Kmeans++ """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 on_partial_result_callback=None, early_terminator=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="inertia", random_state=random_state, id=id,
                         on_partial_result_callback=on_partial_result_callback, early_terminator=early_terminator, verbose=verbose)


class HGPA_PecK(ProgressiveEnsembleClustering):
    """ HGPA Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 on_partial_result_callback=None, early_terminator=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="hgpa", random_state=random_state, id=id,
                         on_partial_result_callback=on_partial_result_callback, early_terminator=early_terminator, verbose=verbose)


class HGPA_PecKPP(ProgressiveEnsembleClustering):
    """ HGPA Based Progressive Ensemble Kmeans++ """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 on_partial_result_callback=None, early_terminator=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="hgpa", random_state=random_state, id=id,
                         on_partial_result_callback=on_partial_result_callback, early_terminator=early_terminator, verbose=verbose)


class MCLA_PecK(ProgressiveEnsembleClustering):
    """ MCLA Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 on_partial_result_callback=None, early_terminator=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means", decision="mcla", random_state=random_state, id=id,
                         partial_result_listener=on_partial_result_callback, early_terminator=early_terminator, verbose=verbose)


class MCLA_PecKPP(ProgressiveEnsembleClustering):
    """ MCLA Based Progressive Ensemble Kmeans """

    def __init__(self, data, n_clusters=2, n_runs=4, random_state=None,
                 on_partial_result_callback=None, early_terminator=None, id=None, verbose=False):
        super().__init__(data, n_clusters=n_clusters, n_runs=n_runs,
                         alg="k-means++", decision="mcla", random_state=random_state, id=id,
                         partial_result_listener=on_partial_result_callback, early_terminator=early_terminator, verbose=verbose)
