"""
data.py
=======

A module for handling data loading and data quality checking.
"""


import os.path
import pandas as pd
from ckd.utils import get_root


def load_test_data(config, preprocessed=True):
    """
    Load the default stest data.

    Parameters
    ----------
    config : ckd.config.Config
        ckd.config.Config object with necessary parameters.
    preprocessed : bool
        If True, will return already preprocessed test data, otherwise will return the raw test data.

    Returns
    -------
    x : pandas.DataFrame
        pandas.DataFrame containing predictor variable data.
    y : pandas.DataFrame
        pandas.DataFrame containing target variable data.
    """

    # load x
    if preprocessed:
        x = pd.read_csv(os.path.join(get_root(), config.x_test_preprocessed_path), index_col=0)
    else:
        x = pd.read_csv(os.path.join(get_root(), config.x_test_path), index_col=0, dtype=object)

    # load y
    y = pd.read_csv(os.path.join(get_root(), config.y_test_path), index_col=0)

    return x, y


def load_train_data(config, preprocessed=True):
    # To be developed later when I decide to add training functionality
    raise NotImplementedError


def load_data(input_data, config):
    """
    Loads input data.

    Based on the parameter input_data, handles data loading differently.

    Parameters
    ----------
    input_data : str, tuple, list, or pandas.DataFrame
        If str, needs to be a valid path to a .csv file.
        If tuple or list, needs to be of length of 2 and contain either:
         - two pandas.DataFrame objects
         - valid paths to two .csv files
        where the first item always corresponds to the predictor variables and the second one to the target.
        If pandas.DataFrame, can either contain the target variable or not.
    config : ckd.config.Config
        ckd.config.Config object with necessary parameters.

    Returns
    -------
    x : pandas.DataFrame
        pandas.DataFrame containing predictor variable data.
    y : pandas.DataFrame or None
        pandas.DataFrame containing target variable data or None if target value is not provided.
    """

    # if 'default', load default data
    if input_data == 'default':
        x, y = load_test_data(config)
        return x, y

    if isinstance(input_data, list) or isinstance(input_data, tuple):
        # assert that input_data has a length of 2
        assert len(input_data) == 2, 'input_data should have a length of 2.'

        # if both are pd.DataFrames, then return them separately
        if isinstance(input_data[0], pd.DataFrame) and isinstance(input_data[1], pd.DataFrame):
            return input_data[0], input_data[1]

        # otherwise they need to be valid .csv paths
        x_path = input_data[0]
        y_path = input_data[1]

        # assert that x_path is a valid .csv file
        assert os.path.isfile(x_path), 'input_data[0] needs to be a valid filepath.'
        assert os.path.splitext(x_path)[1] == '.csv', 'input_data[0] needs to be a .csv file'

        # assert that y_path is a valid .csv file
        assert os.path.isfile(y_path), 'input_data[1] needs to be a valid filepath.'
        assert os.path.splitext(y_path)[1] == '.csv', 'input_data[1] needs to be a .csv file'

        x = pd.read_csv(x_path, index_col=0, dtype=object)
        y = pd.read_csv(y_path, index_col=0, dtype=object)

        return x, y

    # if pandas.DataFrame
    if isinstance(input_data, pd.DataFrame):
        pass
    # else, make sure it's a path and load it as a pandas.DataFrame
    elif os.path.isfile(input_data):
        # make sure it's a .csv file
        assert os.path.splitext(input_data)[1] == '.csv', 'input_data needs to be a .csv file'
        # load the data, assume first column is the index
        input_data = pd.read_csv(input_data, index_col=0, dtype=object)
    else:
        raise ValueError('Invalid input_data.')

    # check if input_data contains the target variable

    if config.target_column_name in input_data.columns:
        x = input_data.drop(columns=config.target_column_name)
        y = input_data[config.target_column_name]
    else:
        x = input_data
        y = None

    return x, y


def check_data(df, config, preprocessed=True):
    """
    Check that given data has the necessary columns for prediction.

    Column order does not matter.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing predictor variable data.
    config : ckd.config.Config
        ckd.config.Config object with necessary parameters.
    preprocessed : bool
        Necessary to decide whether to check for raw or preprocessed column names.


    Returns
    -------
    check_status : bool
        Will always return true. If columns don't match, will raise an AssertionError
    """
    if preprocessed:
        column_names = config.column_names_preprocessed
    else:
        column_names = config.column_names

    # if something is wrong raise an error with a helpful error message
    assert set(df.columns) == set(column_names), 'Invalid column names.'

    check_status = True
    return check_status
