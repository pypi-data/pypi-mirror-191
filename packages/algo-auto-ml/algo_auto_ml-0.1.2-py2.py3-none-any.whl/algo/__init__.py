"""
Algo library

AutoML library for binary classification and regression tasks
Licence: MIT
"""

__author__ = "Pavel Lyulchak"
__version__ = "0.1.2"

from . import automl
from . import features
from . import  ml
from . import task


__all__ = [
    automl,
    features,
    ml,
    task
]
