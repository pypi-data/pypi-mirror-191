"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 24
Date: April 2022
Python: 3.7.7
"""


import numpy as np


def computeStatisticalMoments(distribution, **kwargs):
    """
    Purpose:


    Parameters:
        -

    Returns:
        -

    Imports:
        - ``import numpy as np``
        -

    Description:


    See Also:
        -
    """

    distribution_shape = distribution.shape
    number_points = distribution_shape[1]

    order = kwargs.get("order", 1)
    weights = kwargs.get("weights", np.ones(number_points) / number_points)

    moments = []

    if order > 0:
        m1 = np.sum(weights * distribution, axis=1)
        moments.append(m1)

        if order > 1:
            centered_distribution = (distribution.T - m1).T
            m2 = np.sum(weights * (centered_distribution[None, :, :] * centered_distribution[:, None, :]), axis=2)
            moments.append(m2)

            if order > 2:
                m3 = np.sum(weights * (centered_distribution[None, :, :] * (centered_distribution[None, :, :] * centered_distribution[:, None, :])[:, :, None, :]), axis=3)
                moments.append(m3)

                if order > 3:
                    m4 = np.sum(weights * (centered_distribution[None, :, :] * (centered_distribution[None, :, :] * (centered_distribution[None, :, :] * centered_distribution[:, None, :])[:, :, None, :])[:, :, :, None, :]), axis=4)
                    moments.append(m4)

    return moments