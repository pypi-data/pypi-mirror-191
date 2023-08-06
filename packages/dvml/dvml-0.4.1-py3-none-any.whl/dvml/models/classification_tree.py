"""
Module for classification tree
"""
import random
from math import ceil, sqrt

import numpy as np

from dvml.models.model import SupervisedModel
from dvml.utils.config_utils import parse_config
from dvml.utils.data_utils import parse_x_ct
from dvml.utils.math_utils import gini_binary, gini_opt_split


def select_features(n_features, n_desired):
    """
    Selects a subset of feature indices based on the desired number

    :param n_features: number of input features
    :param n_desired: desired # of features ('sqrt', 'all', or an integer)
    :return: list of feature indices with the desired size
    """
    feature_inds = list(range(n_features))
    if n_desired == "all":
        features = feature_inds
    elif n_desired == "sqrt":
        n_feats = ceil(sqrt(n_features))
        features = sorted(random.sample(feature_inds, n_feats))
    else:
        n_feats = min([int(n_desired), len(feature_inds)])
        features = sorted(random.sample(feature_inds, n_feats))

    return features


def split_data_boundary(x_in, y_in, feat_ind, boundary):
    """
    Splits dataset according to a given feature and boundary

    :param x_in: numpy matrix (or equivalent) of input features
    :param y_in: 1-D numpy array (or equivalent) of target variable
    :param feat_ind: index of feature to split by
    :param boundary: boundary value to split by
    :return: (x_left, y_left, x_right, y_right) split datasets
    """
    # Split the dataset according to the decision
    x_left = x_in[x_in[:, feat_ind] < boundary, :]
    y_left = y_in[x_in[:, feat_ind] < boundary]
    x_right = x_in[x_in[:, feat_ind] > boundary, :]
    y_right = y_in[x_in[:, feat_ind] > boundary]

    return x_left, y_left, x_right, y_right


def split_node(node_list, cur_node, x_node, y_node, node_conf):
    """
    Trains a node and adds its successors (if any) to the node traversal list

    :param node_list: list of nodes to traverse
    :param cur_node: node to be trained and split
    :param x_node: input features for the given node
    :param y_node: input target variable for the given node
    :param node_conf: configuration of the given node
    :return:
    """
    # Train the node
    cur_node_out = cur_node.train(x_node, y_node, node_conf)

    if cur_node_out != -1:
        # The node was not a leaf, create successors
        node_left = ClassificationTreeNode(depth=cur_node.depth + 1)
        node_right = ClassificationTreeNode(depth=cur_node.depth + 1)
        # Attach successors to current node
        cur_node.left = node_left
        cur_node.right = node_right
        # Add successors to node list
        node_list.append((node_left, cur_node_out[0], cur_node_out[1]))
        node_list.append((node_right, cur_node_out[2], cur_node_out[3]))


class ClassificationTreeNode(SupervisedModel):
    """
    Individual node for a classification tree
    """

    DEFAULT_CONF = {
        "n_features": "all",  # Can be either "all", "sqrt", or a number
        "leaf_node": False,
    }

    def __init__(self, return_val=0.5, depth=1):
        # Define the left and right successors, set to empty to start with
        self.left = None
        self.right = None
        # Set a default value, in case it becomes a leaf node
        # The training process will either define successors, or update the return value
        self.return_val = return_val
        # Initialize a dummy decision function
        self.decision = {
            "feature": 0,  # The index of the feature used in the decision
            "boundary": 0,  # The boundary value that decides between left/right successor
        }
        # Set the depth
        self.depth = depth

    def predict(self, x_in):
        # Convert x_in to a numpy array
        x_form = parse_x_ct(x_in)

        # Compute the prediction for each row of the dataset, and collect them into a vector
        return np.apply_along_axis(self.predict_one, axis=1, arr=x_form)

    def predict_one(self, x_vec):
        """

        :param x_vec: 1-D array of features
        :return: prediction for the input features vector
        """
        # If either successor is not defined, return the existing return value
        if self.left is None or self.right is None:
            return self.return_val
        # Otherwise, apply the decision function and collect the return value from the successor
        if x_vec[self.decision["feature"]] < self.decision["boundary"]:
            return self.left.predict_one(x_vec)
        return self.right.predict_one(x_vec)

    def train(self, x_train, y_train, conf: dict = None):
        # Parse config
        parsed_config = parse_config(conf, self.DEFAULT_CONF)
        # Convert x_in to a numpy array
        x_form = parse_x_ct(x_train)
        # Convert y to a numpy vector
        y_form = np.array(y_train)

        # Check if it's a leaf node (or y is constant). If so, compute a return value
        if parsed_config["leaf_node"] or np.sum(y_form) in [0, len(y_form)]:
            self.return_val = np.mean(y_form)
            return -1

        # Select the list of features to be tested
        features = select_features(len(x_form[0, :]), parsed_config["n_features"])

        # For each feature in the list, compute a good boundary
        boundaries = [gini_opt_split(x_form[:, feat], y_form) for feat in features]

        # Find the best boundary
        opt_boundary, opt_gini = min(boundaries, key=lambda bdr: bdr[1])
        # If there's no improvement, compute a return value
        if opt_gini >= gini_binary(y_form):
            self.return_val = np.mean(y_form)
            return -1

        # Otherwise, extract the best feature and proceed
        opt_feature = features[boundaries.index((opt_boundary, opt_gini))]

        # Overwrite the decision
        self.decision = {
            "feature": opt_feature,
            "boundary": opt_boundary,
        }

        # Split the dataset according to the decision
        return split_data_boundary(x_form, y_form, opt_feature, opt_boundary)


class ClassificationTreeModel(SupervisedModel):
    """
    Classification tree model class. Builds the model through
    individual nodes, depth-first
    """

    DEFAULT_CONF = {
        "n_features": "all",  # Can be either "all", "sqrt", or a number
        "max_depth": None,
    }

    def __init__(self):
        self.root_node = ClassificationTreeNode()

    def train(
        self, x_train, y_train, conf: dict = None
    ):  # pylint: disable=too-many-locals
        # Parse config
        parsed_config = parse_config(conf, self.DEFAULT_CONF)
        # Convert x_in to a numpy array
        x_form = parse_x_ct(x_train)
        # Convert y to a numpy vector
        y_form = np.array(y_train)

        # Create the list to traverse depth-first
        node_list = [(self.root_node, x_form, y_form)]

        # Traverse the list, training each node until none are left
        while len(node_list) > 0:
            cur_node, x_node, y_node = node_list.pop()

            # Create config for node training
            is_leaf = False
            if (
                parsed_config["max_depth"] is not None
                and cur_node.depth >= parsed_config["max_depth"]
            ):
                is_leaf = True
            node_conf = {
                "n_features": parsed_config["n_features"],
                "leaf_node": is_leaf,
            }

            # Train/split the node
            split_node(node_list, cur_node, x_node, y_node, node_conf)

    def predict(self, x_in):
        return self.root_node.predict(x_in)

    def predict_th(self, x_in, threshold=0.5):
        """
        Predicts then applies a threshold

        :param x_in: numpy matrix (or equivalent) of features
        :param threshold: classification threshold. Default=0.5
        :return: 1-D array of binary predictions
        """
        return np.array(
            [0 if y_pred < threshold else 1 for y_pred in self.predict(x_in)]
        )

    def get_depth(self):
        """
        Returns the depth of the tree

        :return: tree depth
        """
        depth = 1

        node_list = [self.root_node]

        while len(node_list) > 0:
            cur_node = node_list.pop()

            depth = max(depth, cur_node.depth)

            if cur_node.left is not None:
                node_list.append(cur_node.left)
            if cur_node.right is not None:
                node_list.append(cur_node.right)

        return depth

    def get_n_nodes(self):
        """
        Returns the number of nodes in the tree

        :return: number of tree nodes
        """
        n_nodes = 0

        node_list = [self.root_node]

        while len(node_list) > 0:
            cur_node = node_list.pop()

            n_nodes += 1

            if cur_node.left is not None:
                node_list.append(cur_node.left)
            if cur_node.right is not None:
                node_list.append(cur_node.right)

        return n_nodes
