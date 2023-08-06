# ckd
ckd is a Python library that provides functionality, default train/test data, and pre-trained models to predict Chronic Kidney Disease status from measurement and/or biomarker data.

## Methods
For information about model development, see the jupyter notebook at ckd/notebooks/CKD_AniKh_Wemanity.ipynb

## Requirements
- pandas (version used: 1.5.3, not tested for other versions)
- scikit-learn (version used: 1.2.0, not tested for other versions)
- fire (version used: 0.5.0, not tested for othe versions)

## Installation

From PyPI:
```commandline
pip install ckd
```

From GitHub:

```python
pip install 'git+https://github.com/AniKhachatryan/ckd.git'
```


## Usage
The ckd library provides default data and pre-trained models but can also work with user-provided data.

The main function is _ckd.predict_ckd()_, which handles the whole prediction flow from data/model to Chronic Kidney Disease status prediction and performance evaluation. 

It is possible to run _ckd.predict_ckd()_ without providing any arguments, in which case it will return the predicted values and performance metrics on the default test set using a pre-trained Logistic Regression Classifier.

The _input_data_ parameter can be either
- 'default' (the default argument value)
- a pandas.DataFrame object that may or may not contain the target variable
- a path to a _.csv_ file that may or may not contain the target variable
- a tuple or list of paths to two _.csv_ files, where the second one contains the target variable. 

It is not necessary to provide the target variable, in which case only the predictions will be returned.

If the input data is not already preprocessed, it is necessary to set the argument _preprocess=True_. By default, missing value imputer and scaler objects pre-trained on the train set will be used, but it is possible to provide custom obejcts through the _config_ argument (see Usage Examples).

The _model_ parameter can be either
- a sklearn.base.BaseEstimator object
- one of {'lr', 'rf', 'rfc'} (case-insensitive), where 'lr' stands for Logistic Regression and 'rf' and 'rfc' stand for Random Forest
- a valid path to a .pkl object of class sklearn.base.BaseEstimator. 

It is necessary that the column names of the input data to match the column names the model expects. The _ckd.Config_ class provides default values for the column names but in case the user-provided data and the model have different column names, it should be provided through the _config_ argument (see Usage Examples).

**Output**: 

The _ckd.predict_ckd()_ function returns
- predictions as numpy.ndarray
- performance metrics as dict (only if target values are provided)
  - accuracy
  - sensitivity/recall
  - specificity
  - precision
  - confusion matrix.

### Call _ckd_ from the command line

The _ckd_ package also provides a command line interface, but the functionality is limited as compared to using the package inside Python. 

More specifically, 
- it does not make sense to use the command line interface without providing the target variable as no output will be generated
- it is not possible to provide a custom config file, because such functionality has not been developed yet.

Please see Usage Examples for more information on how to use the command line interface.


## Usage Examples
1. Call _ckd.predict_ckd()_ without providing any arguments. This will use the default test data and the pre-trained Logistic Regression model for prediction and evaluation. 
```python
import ckd
y_predicted, evaluation_dict = ckd.predict_ckd()
```
2. Provide custom input data
```python
import ckd

path_to_x = '/path/to/x.csv'
path_to_y = '/path/to/y.csv'

# provide target labels
y_predicted, evaluation_dict = ckd.predict_ckd(input_data=(path_to_x, path_to_y))

# don't provide labels
y_predicted = ckd.predict_ckd(input_data=path_to_x)
```



3. Provide custom model
```python
import ckd

# use default data but custom model
path_to_model = '/path/to/model.pkl'
y_predicted, evaluation_dict = ckd.predict_ckd(model=path_to_model)
```
4. Custom _config_

More advanced analyses can be done by providing a 
custom _config_ argument. For example, if we want to use a 
custom model with custom data that has different predictor
variables, then we can modify the config file like in the
following example.

```python
import ckd

# set the user-provided column names
column_names_preprocessed = ('colname1', 'colname2', 'colname3')
column_names_cat = ()
column_names_num = column_names_preprocessed

# set the target variable column name, default: class
target_column_name = 'status'

# user-provided model
path_to_model = '/path/to/model.pkl'

# user-provided data
path_to_x = '/path/to/x.csv'
path_to_y = '/path/to/y.csv'

# create a ckd.Config instance
config = ckd.Config(column_names_preprocessed=column_names_preprocessed,
                    column_names_num=column_names_num,
                    column_names_cat=column_names_cat, 
                    target_column_name=target_column_name)


y_predicted, evaluation_dict = ckd.predict_ckd(input_data=(path_to_x, path_to_y), 
                                               model=path_to_model, 
                                               config=config)

```

It is also possible to provide custom missing value imputer or scaler objects in a similar fashion. For more information on all available parameters of the _ckd.Config_ class please see
```python
import ckd
help(ckd.Config)
```

### Command line interface usage examples

1. Call _ckd_ from the command line without any arguments. This is equivalent to calling _ckd.predict_ckd()_ without any arguments from inside Python.
```bash
# default
ckd
```

2. Provide _input_data_ and _preprocess_
```bash
# predictor and target variables are in one .csv file and data needs to be preprocessed
ckd --input_data '/path/to/data.csv' --preprocess True

# predictor and target variables are in two .csv files
ckd --input_data '/path/to/X.csv' --target '/path/to/y.csv'
```

3. Choose a different model or provide a custom one
```bash
# choose Random Forest Classifier instead of the defautl Logistic Regression
ckd --model 'rf'

# provide custom model
ckd --model '/path/to/model.pkl'
```

## Support
Do not hesitate to contact Ani (ani.d.khachatryan@gmail.com) for any questions related to this Python library.

## License
MIT License