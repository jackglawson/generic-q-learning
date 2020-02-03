from statistics import NormalDist
from scipy.integrate import quad
from dataclasses import dataclass
import numpy as np


def get_normal_dist_cdf(mu, sigma, x):
    return NormalDist(mu=mu, sigma=sigma).cdf(x)


def get_normal_dist_pdf(mu, sigma, x):
    return NormalDist(mu=mu, sigma=sigma).pdf(x)


def get_prob_q2_greater_than_q1(mu1, sigma1, mu2, sigma2):
    if sigma1 == sigma2 == 0:
        if mu1 == mu2:
            return 0.5
        elif mu1 < mu2:
            return 1
        else:
            return 0
    elif sigma1 == 0:
        return 1 - get_normal_dist_cdf(mu2, sigma2, mu1)
    elif sigma2 == 0:
        return get_normal_dist_cdf(mu1, sigma1, mu2)

    @dataclass(frozen=True)
    class Func:
        mu1: float
        sigma1: float
        mu2: float
        sigma2: float

        def __call__(self, x):
            p_1 = get_normal_dist_pdf(self.mu1, self.sigma1, x)
            f_2 = get_normal_dist_cdf(self.mu2, self.sigma2, x)
            return p_1 * (1 - f_2)

    func = Func(mu1, sigma1, mu2, sigma2)
    result, error = quad(func, -np.inf, np.inf)[0:2]
    assert error < 1e-5, 'Error is too high. mu1 {}, sigma1 {}, mu2 {}, sigma2 {}, Result: {}, Error: {}'.format(mu1, sigma1, mu2, sigma2, result, error)
    return result
