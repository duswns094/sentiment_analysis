import pandas as pd
import numpy as np

import re
import os
import pickle
import dill # for saving a function as a file
import logging # for changing the tf's logging level


import tensorflow as tf
import tensorflow_addons as tfa

import transformers
from transformers import TFBertModel
import sentencepiece as spm
from tokenization_kobert import KoBertTokenizer


def model_load():
    # 1) Load the Model-builder function
    with open('model_koBERTfunction_v1.pkl', 'rb') as f: # 이번 실습에서 변경되었습니다
        create_model = dill.loads(pickle.load(f)) # use dill to pickle a python function

    # 2) Create the model & load the Model-weights (from checkpoint file)
    model = create_model(max_length=128)
    model.load_weights(filepath='best_kobert_weights.h5')

    return model

