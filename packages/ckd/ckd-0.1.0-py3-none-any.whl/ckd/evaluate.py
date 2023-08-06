"""
evaluate.py
===========

A module for evaluating the predictions.
"""

from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix


def evaluate(y_true, y_predicted, verbose=True):
    """
    Evaluates predictions.

    Parameters
    ----------
    y_true : 1d array-like
        Ground truth (correct) labels.
    y_predicted : 1d array-like
        Predicted labels, as returned by a classifier.

    Returns
    -------
    performance_metrics : dict
        A dictionary containing several classifier performance metrics:
        - accuracy
        - sensitivitiy/recall
        - specificity
        - precision
        - confusion matrix

    """

    # assert that the lengths of y_true and y_predicted are equal
    assert len(y_true) == len(y_predicted), 'y_true and y_predicted lengths should match.'

    # compute performance metrics
    accuracy = accuracy_score(y_true, y_predicted)
    recall_sensitivity = recall_score(y_true, y_predicted, pos_label='ckd')
    specificity = recall_score(y_true, y_predicted, pos_label='notckd')
    precision = precision_score(y_true, y_predicted, pos_label='ckd')
    confusion_mat = confusion_matrix(y_true, y_predicted)

    # create a dict
    performance_metrics = {
        'accuracy': accuracy,
        'recall_sensitivity': recall_sensitivity,
        'specificity': specificity,
        'precision': precision,
        'confusion_mat': confusion_mat
    }

    if verbose:
        # print some metrics
        print(f'Classification performance metrics:\n'
              f'Accuracy: {accuracy}\n'
              f'Recall (sensitivity): {recall_sensitivity}\n'
              f'Specificity: {specificity}\n'
              f'Precision: {precision}\n')

    return performance_metrics
