#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Module for prediction in sound files.

Author: Erika Peláez
MIT license

This module contains all the functions to do feature extraction on your dataset for classification with Machine Learning.
"""

import pickle
import pandas as pd

def load_pkl(file_path):
    """Load serialized model with pickle library.

    Parameters
    ----------
    file_path: str Path to the serialized model.

    Returns
    -------
    Trained model object.

    """
    with open(file_path) as model:
        clf = pickle.load(model)
        return clf

def predict_rf(model, data, file_names):
    """Get prediction and probability of a class in a pandas data frame.

    Parameters
    ----------
    model: obj Trained model.
    data: array like data to be predicted
    file_names: list with the names of the files for each data point

    Returns
    -------
    Pandas data frame with predictions for each file.
    
    """
    predictions = model.predict(data)
    probabilities = model.predict_proba(data)
    result = pd.DataFrame({'file_name':file_names,
                           'prediction': predictions,
                           'probabilities': probabilities})
    return result