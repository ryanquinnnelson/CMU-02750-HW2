import numpy as np
import packages.dh.helper as helper
import random


# tested
def _proportional_selection(P, T, num_samples):
    """
    Select a node v from the pruning, proportional to the size of subtree rooted at v.
    :param P: array, represents current pruning
    :param T: Tree data structure
    :param num_samples: Number of samples in the data
    :return:
    """

    # for each subtree in P, get the number of leaf nodes in that subtree
    num_leaves = np.zeros(len(P))
    for i in range(len(P)):
        leaves = helper.get_leaves([], P[i], T, num_samples)
        num_leaves[i] = (len(leaves))

    # set weights wv for each node v in P:  wv = # leaves Tv / # leaves T
    p = num_leaves / num_samples
    selected = np.random.choice(P, 1, p=p)
    return selected[0]


def _confidence_adjusted_selection(P, T, num_samples, pHat1):
    """
    Select a node from P biasing towards choosing nodes in areas where the observed labels are less pure.

    :param T:
    :param num_samples:
    :param pHat1:
    :return:
    """



    return 0


def select_case_1(X, y_true, T, budget, batch_size):
    """

    :param X: a x b matrix, data samples
    :param y_true: a x 1 vector, true labels for samples
    :param T: Tree data structure
    :param budget: Number of iterations allowed
    :param batch_size: Number of queries per iteration
    :return:
    """

    # define variables
    num_nodes = len(T[1])  # total nodes in T
    num_samples = len(X)  # total samples in data

    # set scaffolds to fill in
    n = np.zeros(num_nodes)  # number of points sampled from each node
    pHat1 = np.zeros(num_nodes)  # empirical label frequency
    L = np.zeros(num_nodes)  # majority label

    # additional
    error = []  # error for each iteration

    # set initial pruning and labeling for root
    root = num_nodes - 1  # index of root
    P = np.array([root])
    L[root] = 1

    # perform i iterations
    for j in range(budget):

        # step 1
        selected_P = set()  # ?? should be set instead of list
        for b in range(batch_size):
            # TODO: select a node from P proportional to the size of subtree rooted at each node (DONE)
            v = _proportional_selection(P, T, num_samples)
            selected_P.add(v)

            # TODO: pick a random leaf node from subtree Tv and query its label (DONE)
            v_leaves = helper.get_leaves([], v, T, num_samples)
            z = random.choice(v_leaves)
            label_z = y_true[z]

            # TODO: update empirical counts and probabilities for all nodes u on path from z to v (DONE)
            n, pHat1 = helper.update_empirical(n, pHat1, v, z, label_z, T)
            # print('pHat1',pHat1)
            # print('n',n)

        # step 2
        for p in selected_P:
            # TODO: update admissible A and compute scores; find best pruning and labeling (DONE)
            P_best, L_best = helper.best_pruning_and_labeling(n, pHat1, p, T, num_samples)

            # TODO: update pruning P and labeling L
            # update pruning
            P_without_s = P[P != p]  # remove p from P using a mask
            P = np.union1d(P_without_s, P_best)

            # assign label L_best to all u in P_best
            for u in P_best:
                L[u] = L_best

        # TODO: temporarily assign labels to every leaf and compute error (DONE)
        L_temp = L.copy()
        for v in P:
            L_temp = helper.assign_labels(L_temp, v, v, T, num_samples)  # assign each leaf in Tv the label L(v)
        error_i = helper.compute_error(L_temp[:num_samples], y_true)  # compute error of leaf nodes only
        error.append(error_i)

    # after all iterations
    # assign final labeling based on best pruning
    for j in range(len(P)):
        L = helper.assign_labels(L, P[j], P[j], T, num_samples)  # assign each leaf in Ti the label L(i)
    return L, np.array(error)


def select_case_2(X, y_true, T, budget, batch_size):
    """

    :param X: a x b matrix, data samples
    :param y_true: a x 1 vector, true labels for samples
    :param T: Tree data structure
    :param budget: Number of iterations allowed
    :param batch_size: Number of queries per iteration
    :return:
    """

    # define variables
    num_nodes = len(T[1])  # total nodes in T
    num_samples = len(X)  # total samples in data

    # set scaffolds to fill in
    n = np.zeros(num_nodes)  # number of points sampled from each node
    pHat1 = np.zeros(num_nodes)  # empirical label frequency
    L = np.zeros(num_nodes)  # majority label

    # additional
    error = []  # error for each iteration

    # set initial pruning and labeling for root
    root = num_nodes - 1  # index of root
    P = np.array([root])
    L[root] = 1

    # perform i iterations
    for j in range(budget):

        # step 1
        selected_P = set()  # ?? should be set instead of list
        for b in range(batch_size):
            # TODO: select a node from P biased  towards choosing nodes in areas where the observed labels are less pure
            v = _confidence_adjusted_selection(P, T, num_samples, pHat1)
            selected_P.add(v)

            # TODO: pick a random leaf node from subtree Tv and query its label (DONE)
            v_leaves = helper.get_leaves([], v, T, num_samples)
            z = random.choice(v_leaves)
            label_z = y_true[z]

            # TODO: update empirical counts and probabilities for all nodes u on path from z to v (DONE)
            n, pHat1 = helper.update_empirical(n, pHat1, v, z, label_z, T)
            # print('pHat1',pHat1)
            # print('n',n)

        # step 2
        for p in selected_P:
            # TODO: update admissible A and compute scores; find best pruning and labeling (DONE)
            P_best, L_best = helper.best_pruning_and_labeling(n, pHat1, p, T, num_samples)

            # TODO: update pruning P and labeling L
            # update pruning
            P_without_s = P[P != p]  # remove p from P using a mask
            P = np.union1d(P_without_s, P_best)

            # assign label L_best to all u in P_best
            for u in P_best:
                L[u] = L_best

        # TODO: temporarily assign labels to every leaf and compute error (DONE)
        L_temp = L.copy()
        for v in P:
            L_temp = helper.assign_labels(L_temp, v, v, T, num_samples)  # assign each leaf in Tv the label L(v)
        error_i = helper.compute_error(L_temp[:num_samples], y_true)  # compute error of leaf nodes only
        error.append(error_i)

    # after all iterations
    # assign final labeling based on best pruning
    for j in range(len(P)):
        L = helper.assign_labels(L, P[j], P[j], T, num_samples)  # assign each leaf in Ti the label L(i)
    return L, np.array(error)
