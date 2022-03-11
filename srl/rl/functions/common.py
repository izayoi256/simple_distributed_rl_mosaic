import random

import numpy as np


def rescaling(x, eps=0.001):
    return np.sign(x) * (np.sqrt(np.abs(x) + 1.0) - 1.0) + eps * x


def inverse_rescaling(x, eps=0.001):
    n = np.sqrt(1.0 + 4.0 * eps * (np.abs(x) + 1.0 + eps)) - 1.0
    n = n / (2.0 * eps)
    return np.sign(x) * ((n ** 2) - 1.0)


def sigmoid(x, a=1):
    return 1 / (1 + np.exp(-a * x))


def create_beta_list(policy_num: int, max_beta=0.3):
    assert policy_num > 0
    beta_list = []
    for i in range(policy_num):
        if i == 0:
            b = 0
        elif i == policy_num - 1:
            b = max_beta
        else:
            b = 10 * (2 * i - (policy_num - 2)) / (policy_num - 2)
            b = max_beta * sigmoid(b)
        beta_list.append(b)
    return beta_list


def create_gamma_list(policy_num: int, gamma0=0.9999, gamma1=0.997, gamma2=0.99):
    assert policy_num > 0
    gamma_list = []
    for i in range(policy_num):
        if i == 0:
            g = gamma0
        elif 1 <= i and i <= 6:
            g = gamma0 + (gamma1 - gamma0) * sigmoid(10 * ((2 * i - 6) / 6))
        elif i == 7:
            g = gamma1
        else:
            g = (policy_num - 9 - (i - 8)) * np.log(1 - gamma1) + (i - 8) * np.log(1 - gamma2)
            g = 1 - np.exp(g / (policy_num - 9))
        gamma_list.append(g)
    return gamma_list


def create_epsilon_list(policy_num: int, epsilon=0.4, alpha=8.0):
    epsilon_list = []
    for i in range(policy_num):
        e = epsilon ** (1 + (i / (policy_num - 1)) * alpha)
        epsilon_list.append(e)
    return epsilon_list


def random_choice_by_probs(probs):
    r = random.random() * sum(probs)

    num = 0
    for i, weight in enumerate(probs):
        num += weight
        if r <= num:
            return i
    # not comming
    raise ValueError


def calc_epsilon_greedy_probs(q, valid_actions, epsilon, nb_actions):
    nb_valid_actions = len(valid_actions)
    if nb_valid_actions == 0:
        return [1 / nb_actions for _ in range(nb_actions)]

    qmax = np.amax(q, axis=0)
    qmax_num = np.count_nonzero(q == qmax)

    probs = []
    for a in range(nb_actions):
        if a in valid_actions:
            prob = epsilon / nb_valid_actions
            if q[a] == qmax:
                prob += (1 - epsilon) / qmax_num
            probs.append(prob)
        else:
            probs.append(0.0)
    return probs