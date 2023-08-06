"""
Module for linear models
"""
from abc import ABC

import numpy as np

from dvml.models.model import SupervisedGradientModel
from dvml.optimization.gradient import GradientDescent
from dvml.utils.config_utils import parse_config
from dvml.utils.data_utils import parse_x_lr
from dvml.utils.math_utils import sigmoid


class LinearModel(SupervisedGradientModel, ABC):
    """
    Linear model abstract class, contains common methods between linear and logistic regression
    """

    DEFAULT_TRAIN_CONF = {
        "gamma": 0.01,
        "n_iter": 1000,
        "verbose": False,
    }

    def __init__(self):
        self.params = None

    def gradient(self, x_in, y_in, params_in=None):
        # Check if parameters were passed
        if params_in is None:
            params_grad = self.params
        # Otherwise, use internal parameters
        else:
            params_grad = np.array(params_in)

        # Convert X to a NumPy array, and format for linear regression
        x_form = parse_x_lr(x_in)

        # Convert y to a NumPy vector
        y_form = np.array(y_in)

        # Compute prediction error
        diff = y_form - self.predict(x_in, params_grad)

        # Compute and return gradient
        return np.dot(-x_form.transpose(), diff)

    def set_params(self, params):
        """
        Sets the model parameters

        :param params: array of desired model parameters
        :return:
        """
        self.params = np.array(params)

    def train(self, x_train, y_train, conf: dict = None):
        """
        Trains the model using gradient descent

        :param x_train: a pandas dataframe or numpy array of model features
        :param y_train: target variable array
        :param conf: training configuration, dict-like object
            gamma (float): learning rate
            n_iter (int): number of iterations of gradient descent to run
            verbose (bool): whether to print intermediate results or not
        :return:
        """

        parsed_conf = parse_config(conf, self.DEFAULT_TRAIN_CONF)
        # Convert X to a NumPy array
        x_form = np.array(x_train)
        # Convert y to a NumPy vector
        y_form = np.array(y_train)

        optimizer = GradientDescent(self)

        params_ini = np.zeros(len(x_train[0]) + 1)

        opt_params = optimizer.optimize(x_form, y_form, params_ini, parsed_conf)

        self.set_params(opt_params)


class LinearRegression(LinearModel):
    """
    Linear regression model, trained with basic gradient descent
    """

    def loss(self, x_in, y_in, params_in=None):
        """
        Loss function to be optimized when training the model.
        For linear regression, the loss is the residual sum of squares

        :param x_in: a pandas dataframe or numpy array of model features
        :param y_in: target variable array
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return: the residual sum of squares for the given input data
        """
        # Check if parameters were passed
        if params_in is None:
            params_loss = self.params
        # Otherwise, use internal parameters
        else:
            params_loss = np.array(params_in)

        # Convert y to a NumPy vector
        y_form = np.array(y_in)

        # Compute prediction error
        diff = y_form - self.predict(x_in, params_loss)

        # Compute and return loss
        return 0.5 * np.inner(diff, diff)

    def predict(self, x_in, params_in=None):
        """
        Prediction function

        :param x_in: a pandas dataframe or numpy array of model features
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return: numpy array of model predictions
        """
        # Check if parameters were passed
        if params_in is None:
            params_pred = self.params
        # Otherwise, use internal parameters
        else:
            params_pred = np.array(params_in)

        # First, check that the model is trained, or at least has parameters
        if params_pred is None:
            raise RuntimeError("Model must be trained before predicting.")

        # Convert X to a NumPy array, and format for linear regression
        x_form = parse_x_lr(x_in)

        return np.dot(x_form, params_pred)


class LogisticRegression(LinearModel):
    """
    Logistic regression model, trained with basic gradient descent
    """

    def loss(self, x_in, y_in, params_in=None):
        """
        Loss function to be optimized when training the model.
        For logistic regression, the loss is the log loss

        :param x_in: a pandas dataframe or numpy array of model features
        :param y_in: target variable array
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return: the log loss for the given input data
        """
        # Check if parameters were passed
        if params_in is None:
            params_loss = self.params
        # Otherwise, use internal parameters
        else:
            params_loss = np.array(params_in)

        # Compure the prediction for the given input and parameters
        y_pred = self.predict(x_in, params_loss)
        # Convert y to a NumPy vector
        y_form = np.array(y_in)

        eps = np.finfo(np.float32).eps * 2

        loss = -np.sum(y_form * np.log(y_pred + eps)) - np.sum(
            (1 - y_form) * np.log(1 - y_pred + eps)
        )

        return loss

    def predict(self, x_in, params_in=None):
        """
        Prediction function

        :param x_in: a pandas dataframe or numpy array of model features
        :param params_in: model parameters. If not passed, will use the trained model parameters
        :return: numpy array of model predictions
        """
        # Check if parameters were passed
        if params_in is None:
            params_pred = self.params
        # Otherwise, use internal parameters
        else:
            params_pred = np.array(params_in)

        # First, check that the model is trained, or at least has parameters
        if params_pred is None:
            raise RuntimeError("Model must be trained before predicting.")

        # Convert X to a NumPy array, and format for logistic regression
        x_form = parse_x_lr(x_in)

        return sigmoid(np.dot(x_form, params_pred))
