"""
Algo library

AutoML library for binary classification and regression tasks
Licence: MIT
"""


from .automl import *
from .features import *
from .ml import *
from .task import *


__all__ = [
    AlgoAutoML,
    Preprocessor,
    ClassificationAlgo,
    RegressionAlgo,
    Task
]
