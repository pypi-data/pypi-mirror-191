"""
Utility functions to handle data
"""
import numpy as np


def parse_x_lr(x_in):
    """
    Parse features data for linear regression, by adding a column of 1s to the left (for intercept)

    :param x_in: numpy array (or equivalent) with the input features
    :return:
    """
    try:
        x_np = np.array(x_in)
        ones = np.ones(len(x_np)).reshape([len(x_np), 1])
    except Exception as exc:
        raise TypeError("The data must be numpy array or equivalent") from exc

    return np.concatenate((ones, x_np), axis=1)


def parse_x_ct(x_in):
    """
    Parse features data for classification tree

    :param x_in: numpy array (or equivalent) with the input features
    :return:
    """
    # Convert x_in to a numpy array
    x_form = np.array(x_in)
    # Make it into a matrix if it was just a vector
    if x_form.ndim == 1:
        x_form = x_form.reshape([1, len(x_form)])

    return x_form
