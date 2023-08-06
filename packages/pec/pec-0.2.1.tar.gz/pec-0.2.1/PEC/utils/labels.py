import numpy as np
from sklearn.metrics import jaccard_score


def best_labels_dtype(max_val):
    """Best dtype for the number of distinct label existing"""
    if max_val <= 127:
        return np.int8
    elif max_val <= 32767:
        return np.int16
    else:
        return np.int32


def adjustLabels(labels, refLabels):
    """
    Adjust labels in order to be robust again permutation of labels with the same clustering.
    Use refLabels as reference.

    !!! IT WORKS ONLY IF labels AND refLabels HAVE THE SAME NUMBER OF CLUSTERS. OTHERWISE IT RETURNS labels
    """
    if refLabels is None:
        return labels.copy()
    if labels is None:
        raise RuntimeError(f"Labels cannot be None")

    uniqueLabels = np.unique(labels)
    uniqueRefLabels = np.unique(refLabels)
    if len(uniqueLabels) != len(uniqueRefLabels):
        print(
            f"WARNING: Different number of clusters in labels ({len(uniqueLabels)}) and refLabel ({len(uniqueRefLabels)}). The function returns labels.")
        return labels.copy()

    k = len(uniqueLabels)
    S = np.full((k, k), 0, dtype=float)  # similarity between clusters and refClusters
    for i in range(k):
        for j in range(k):
            S[i, j] = jaccard_score(labels == uniqueLabels[i], refLabels == uniqueRefLabels[j])
            # sklearn.metrics.pairwise.euclidean_distances

    mapping = [None] * k
    while mapping.count(None) != 0:
        i, j = np.unravel_index(S.argmax(), S.shape)  # index of max value of similarity
        S[i] = -1  # remove i from matrix
        S[:, j] = -1  # remove j from matrix
        # S[i,j] = -1
        mapping[i] = j  # uniqueLabels[i] is mapped to refLabel[j]

    result = labels.copy()
    for i, j in enumerate(mapping):
        l = uniqueLabels[i]
        r = uniqueRefLabels[j]
        result[labels == l] = r  # assign mapped label

    return result


def adjustPartitions(partitions, refLabels):
    fn = lambda p: adjustLabels(p, refLabels)
    adjPart = np.apply_along_axis(fn, 1, partitions)
    return adjPart
