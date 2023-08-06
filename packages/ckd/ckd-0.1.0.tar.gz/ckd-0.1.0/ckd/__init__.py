"""
ckd
===

ckd is a package with functionality to predict the presence/absence of Chronic Kidney Disease
using pre-trained Logistic Regression, Random Forest or custom user-provided models.
"""


from ckd.predict import predict_ckd
from ckd.config import Config
from ckd.data import load_data, load_test_data, load_train_data, check_data
from ckd.evaluate import evaluate
from ckd.preprocess import preprocess_data


__version__ = '0.1.0'

