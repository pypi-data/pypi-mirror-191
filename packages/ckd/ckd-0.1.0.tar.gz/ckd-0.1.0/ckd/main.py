import os
import ckd
from ckd.utils import get_root

if __name__ == '__main__':

    pkg_path = get_root()
    data_dir = os.path.join(pkg_path, 'files/data')
    x_raw_path = os.path.join(data_dir, 'X_test_raw.csv')
    x_preprocessed_path = os.path.join(data_dir, 'X_test_preprocessed.csv')
    y_path = os.path.join(data_dir, 'y_test.csv')

    # default
    y_predicted, evaluation_dict = ckd.predict_ckd()

    # raw
    y_predicted_raw, evaluation_dic_raw = ckd.predict_ckd(input_data=(x_raw_path, y_path), preprocess=True)

    # preprocessed
    y_predicted, evaluation_dict = ckd.predict_ckd(input_data=(x_preprocessed_path, y_path))

    # don't evaluate
    y_predicted = ckd.predict_ckd(evaluate_predictions=False)

    # different model (Random Forest)
    y_predicted, evaluation_dict = ckd.predict_ckd(model='rfc')
