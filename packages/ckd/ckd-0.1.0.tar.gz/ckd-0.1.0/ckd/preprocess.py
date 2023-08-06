"""
preprocess.py
=============

A module to handle data preprocessing.
"""


import os
import pickle
import pandas as pd
from ckd.data import check_data
from ckd.utils import get_root


def preprocess_data(df, config, test=True):

    """
    Preprocess given data.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data to preprocess.
    config : ckd.config.Config
        ckd.config.Config object with necessary parameters.
    test : bool
        If Frue, will use imputer and scaler objects fit on the training data.
        If False, will .fit_transform() on the given data.

    Returns
    -------
    df : pandas.DataFrame
        Preprocessed data.

    """

    # params
    missing_value_imputer_path = os.path.join(get_root(), config.missing_value_imputer_path)
    robust_scaler_path = os.path.join(get_root(), config.robust_scaler_path)
    column_names_cat = list(config.column_names_cat)
    # column_names_num = list(config.column_names_num)
    column_names_preprocessed = set(config.column_names_preprocessed)

    # assert column names
    assert check_data(df, config, preprocessed=False)

    # missing values
    missing_value_imputer = pickle.load(open(missing_value_imputer_path, 'rb'))
    column_names_new = [column_name[5:] for column_name in missing_value_imputer.get_feature_names_out()]
    if test:
        # transform
        df = pd.DataFrame(missing_value_imputer.transform(df), index=df.index, columns=column_names_new)
    else:
        # fit transform
        df = pd.DataFrame(missing_value_imputer.fit_transform(df), index=df.index, columns=column_names_new)

    # encode categorical columns
    df = pd.get_dummies(df, columns=column_names_cat, drop_first=True)

    # some columns might be missing so make sure to add them
    missing_columns = column_names_preprocessed - set(df.columns)
    for col in missing_columns:
        df[col] = 0

    # scale features
    robust_scaler = pickle.load(open(robust_scaler_path, 'rb'))
    if test:
        # transform
        df[robust_scaler.feature_names_in_] = robust_scaler.transform(df[robust_scaler.feature_names_in_])
    else:
        # fit transform
        df[robust_scaler.feature_names_in_] = robust_scaler.fit_transform(df[robust_scaler.feature_names_in_])

    return df
