"""
Metrics for classification models
"""
import numpy as np


def accuracy(y_real, y_pred):
    """
    Computes the accuracy of a prediction

    :param y_real: 1-D numpy array (or equivalent) of real values of the binary target variable
    :param y_pred: 1-D numpy array (or equivalent) of boolean model predictions
    :return: measured accuracy
    """
    yrf = np.array(y_real)
    ypf = np.array(y_pred)

    return np.sum((yrf - ypf) == 0) / len(y_real)
