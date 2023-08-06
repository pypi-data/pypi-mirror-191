"""
Module for gradient-descent optimizers
"""
from dvml.models.model import SupervisedGradientModel
from dvml.utils.config_utils import parse_config


class GradientDescent:  # pylint: disable=too-few-public-methods
    """
    Basic gradient descent optimizer

    :param model: the model to optimize
    """

    DEFAULT_CONF = {
        "gamma": 0.01,
        "n_iter": 1000,
        "verbose": True,
    }

    def __init__(self, model: SupervisedGradientModel):
        self.model = model

    def optimize(self, x_in, y_in, params_ini, conf: dict = None):
        """
        Optimizes model parameters based on the input data provided.

        :param x_in: a pandas dataframe or numpy array of model features
        :param y_in: target variable array
        :param params_ini: initial model parameters
        :param conf: dict-like object of model parameters:
            gamma (float): learning rate
            n_iter (int): number of iterations of gradient descent to run
            verbose (bool): whether to print intermediate results or not
        :return:
            params (numpy array): optimized model parameters
        """
        parsed_conf = parse_config(conf, self.DEFAULT_CONF)

        print("Starting gradient descent optimization...")
        loss_ini = self.model.loss(x_in, y_in, params_ini)
        print(f"Initial loss: {loss_ini}")

        params = params_ini
        loss = -1

        for ind in range(parsed_conf["n_iter"]):
            grad = self.model.gradient(x_in, y_in, params)
            params = params - (parsed_conf["gamma"] * grad)
            loss = self.model.loss(x_in, y_in, params)
            if parsed_conf["verbose"]:
                print(f"[{ind+1}/{parsed_conf['n_iter']}] Loss: {loss}")

        print(f"Final loss: {loss}")

        return params
