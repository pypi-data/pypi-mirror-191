"""
Module with the template classes for models
"""
from abc import ABC, abstractmethod

import numpy as np


class Model(ABC):  # pylint: disable=too-few-public-methods
    """
    Generic model class
    """

    @abstractmethod
    def predict(self, x_in):
        """
        Prediction function
        :param x_in: a pandas dataframe or numpy array of model features
        :return:
        """


class SupervisedModel(Model):
    """
    Generic supervised model class
    """

    @abstractmethod
    def train(self, x_train, y_train, conf: dict = None):
        """

        :param x_train: a pandas dataframe or numpy array of model features
        :param y_train: target variable array
        :param conf: training configuration, dict-like object
        :return:
        """


class SupervisedGradientModel(SupervisedModel):
    """
    Generic supervised model class,
    With a differentiable loss function
    """

    @abstractmethod
    def predict(self, x_in, params_in=None):
        """
        Prediction function, with optional parameter passing for gradient computations

        :param x_in: a pandas dataframe or numpy array of model features
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return:
        """

    @abstractmethod
    def loss(self, x_in, y_in, params_in=None):
        """
        Loss function to be optimized when training the model

        :param x_in: a pandas dataframe or numpy array of model features
        :param y_in: target variable array
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return:
        """

    @abstractmethod
    def gradient(self, x_in, y_in, params_in=None):
        """
        Gradient of the loss function, used in gradient descent to train the model

        :param x_in: a pandas dataframe or numpy array of model features
        :param y_in: target variable array
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return: numpy array with the gradient of the loss function for the given input data
        """


class UnsupervisedModel(Model):
    """
    Generic unsupervised model class
    """

    @abstractmethod
    def train(self, x_train):
        """

        :param x_train: a pandas dataframe or numpy array of model features
        :return:
        """


class ConstantModel(Model):  # pylint: disable=too-few-public-methods
    """
    Constant model: dummy model for basic tests.
    """

    def __init__(self, y_val):
        self.y_val = y_val

    def predict(self, x_in):
        return np.ones(len(x_in)) * self.y_val
