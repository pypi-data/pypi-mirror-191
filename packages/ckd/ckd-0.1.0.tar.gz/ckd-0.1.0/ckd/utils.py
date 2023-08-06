"""
utils.py
========

A module to prive utility functions.
"""


import os
import pickle
import sklearn


def load_model(model, config):

    """
    Load the model.

    Parameters
    ----------
    model : str, sklearn.base.BaseEstimator
        If str, can be either
        - one of {'lr', 'rf', 'rfc'} (case-insensitive)
        - a valid path to a .pkl object of class sklearn.base.BaseEstimator
    config : ckd.config.Config
        ckd.config.Config object with necessary parameters.

    Returns
    -------
    model_loaded : sklearn.base.BaseEstimator

    """

    # check if model is already a sklearn model
    if isinstance(model, sklearn.base.BaseEstimator):
        return model

    # otherwise assert that model is a string
    assert isinstance(model, str), 'model needs to be either str or sklearn.base.BaseEstimator'

    if model.lower() == 'lr':
        model_path = os.path.join(get_root(), config.model_path_lr)
        model_loaded = pickle.load(open(model_path, 'rb'))
    elif model.lower() in ['rf', 'rfc']:
        model_path = os.path.join(get_root(), config.model_path_rf)
        model_loaded = pickle.load(open(model_path, 'rb'))
    elif os.path.isfile(model):
        # assert that the path is a pickle file a pickle file
        assert os.path.splitext(model)[1] == '.pkl'
        # load the model
        model_loaded = pickle.load(open(model, 'rb'))
        # assert that it's a sklearn.base.BaseEstimator
        assert isinstance(model, sklearn.base.BaseEstimator), 'model needs to be sklearn.base.BaseEstimator'
    else:
        raise ValueError('Invalid model argument passed.')

    return model_loaded


def get_root():

    """
    Return the absolute path to the package folder.

    Returns
    -------
    root_path : str
        Absolute path to the package folder.

    """

    # return the absolute path to the package directory
    root_path = os.path.dirname(__file__)
    return root_path
