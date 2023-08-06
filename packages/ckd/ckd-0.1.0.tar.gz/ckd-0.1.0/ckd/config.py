"""
Config
======

A generic class for controlling the main parameters for CKD prediction.
"""

default_column_names = ('age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu', 'sc', 'sod', 'pot',
                        'hemo', 'pcv', 'wbcc', 'rbcc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane')
default_column_names_preprocessed = ('age', 'bp', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc',
                                     'sg_1.010', 'sg_1.015', 'sg_1.020', 'sg_1.025', 'al_1', 'al_2', 'al_3', 'al_4',
                                     'al_5', 'su_1', 'su_2', 'su_3', 'su_4', 'su_5', 'rbc_normal', 'pc_normal',
                                     'pcc_present', 'ba_present', 'htn_yes', 'dm_yes', 'cad_yes', 'appet_poor',
                                     'pe_yes', 'ane_yes')
default_column_names_num = ('age', 'bp', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc')
default_column_names_cat = ('sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane')


class Config:
    def __init__(self,
                 x_train_path='files/data/X_train_raw.csv',
                 x_test_path='files/data/X_test_raw.csv',
                 x_train_preprocessed_path='files/data/X_train_preprocessed.csv',
                 x_test_preprocessed_path='files/data/X_test_preprocessed.csv',
                 y_train_path='files/data/y_train.csv',
                 y_test_path='files/data/y_test.csv',
                 target_column_name='class',
                 model_path_lr='files/models/lr_clf.pkl',
                 model_path_rf='files/models/rf_clf.pkl',
                 missing_value_imputer_path='files/models/mv_imputer.pkl',
                 robust_scaler_path='files/models/rb_scaler.pkl',
                 column_names=default_column_names,
                 column_names_preprocessed=default_column_names_preprocessed,
                 column_names_cat=default_column_names_cat,
                 column_names_num=default_column_names_num):
        """
        A config class to handle parameters.

        Parameters
        ----------
        x_train_path : str
            Path to the raw X_train .csv.
        x_test_path : str
            Path to the raw X_test .csv.
        x_train_preprocessed_path : str
            Path to the preprocessed X_train .csv.
        x_test_preprocessed_path : str
            Path to the preprocessed X_test .csv.
        y_train_path : str
            Path to the y_train .csv
        y_test_path : str
            Path to the y_test .csv
        target_column_name : str
            Name of the target column.
        model_path_lr : str
            Path to the trained Logistic Regression model .pkl file.
        model_path_rf : str
            Path to the trained Random Forest Classifier model .pkl file.
        missing_value_imputer_path : str
            Path to the trained missing value imputer .pkl file.
        robust_scaler_path : str
            Path to the trained robust scaler .pkl file.
        column_names : set
            Set of raw column names.
        column_names_preprocessed : set
            Set of preprocessed column names.
        column_names_cat : set
            Set of raw categorical column names.
        column_names_num : set
            Set of raw numerical column names (same as preprocessed).
        """

        self.x_train_path = x_train_path
        self.x_test_path = x_test_path
        self.x_train_preprocessed_path = x_train_preprocessed_path
        self.x_test_preprocessed_path = x_test_preprocessed_path
        self.y_train_path = y_train_path
        self.y_test_path = y_test_path
        self.target_column_name = target_column_name
        self.model_path_lr = model_path_lr
        self.model_path_rf = model_path_rf
        self.missing_value_imputer_path = missing_value_imputer_path
        self.robust_scaler_path = robust_scaler_path
        self.column_names = column_names
        self.column_names_preprocessed = column_names_preprocessed
        self.column_names_cat = column_names_cat
        self.column_names_num = column_names_num
