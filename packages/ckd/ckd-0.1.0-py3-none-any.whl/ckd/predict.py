"""
predict.py
==========

A module to handle predictions.
"""


from ckd.config import Config
from ckd.data import load_data, check_data
from ckd.preprocess import preprocess_data
from ckd.utils import load_model
from ckd.evaluate import evaluate


def predict_ckd(input_data='default', model='LR', preprocess=False,
                evaluate_predictions=True, config=Config()):

    """
    Perform predictions on input_data.

    Parameters
    ----------
    input_data : str, tuple, list, or pandas.DataFrame
        If str, needs to be a valid path to a .csv file.
        If tuple or list, needs to be of length of 2 and contain either:
         - two pandas.DataFrame objects
         - valid paths to two .csv files
        where the first item always corresponds to the predictor variables and the second one to the target.
        If pandas.DataFrame, can either contain the target variable or not.
    model : str, sklearn.base.BaseEstimator
        If str, can be either
        - one of {'lr', 'rf', 'rfc'} (case-insensitive)
        - a valid path to a .pkl object of class sklearn.base.BaseEstimator
    preprocess : bool
        Whether preprocess input_data.
    evaluate_predictions : bool
        Whether to evaluate predictions. Target variable needs to be available.

    config : ckd.config.Config
        ckd.config.Config object with necessary parameters.

    Returns
    -------
    y_predicted : numpy.ndarray
        numpy.ndarray of predicted classes.
    evaluation_dict : dict
        A dictionary containing several classifier performance metrics:
        - accuracy
        - sensitivitiy/recall
        - specificity
        - precision
        - confusion matrix

    """

    # input_data is either 'default', a path, a pandas.DataFrame
    x, y = load_data(input_data, config)

    # if target data is not available, set evaluate_predictions to false
    if y is None:
        evaluate_predictions = False

    # check that data has the right format (columns)
    assert check_data(x, config, preprocessed=not preprocess)

    if preprocess:
        x = preprocess_data(x, config)

    # handle model
    model = load_model(model, config)

    # predict
    y_predicted = model.predict(x[model.feature_names_in_])

    evaluation_dict = None
    if evaluate_predictions:
        # make sure we have valid y_true
        assert y is not None, 'Target variable not provided. Cannot evaluate predictions.'
        evaluation_dict = evaluate(y, y_predicted)

    # return predictions and performance metrics dict
    if evaluation_dict is not None:
        return y_predicted, evaluation_dict
    else:
        return y_predicted
