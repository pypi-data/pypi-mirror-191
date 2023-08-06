"""
cli.py
======

Command-line interface support.
"""

import fire
from ckd import predict_ckd


def cli_func(input_data: str = None, target: str = None, model: str = 'lr', preprocess: bool = False):
    """
    Add command line functionality.

    Does not support custom config argument.

    Parameters
    ----------
    input_data : str
    target : str
    model : str
    preprocess : bool

    Returns
    -------

    """
    if input_data:
        if target:
            input_data = (input_data, target)
    else:
        input_data = 'default'

    predict_ckd(input_data=input_data, model=model, preprocess=preprocess)


def main():
    fire.Fire(cli_func)
