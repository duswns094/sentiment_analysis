import pandas as pd
import numpy as np

import re
import os
import pickle
import dill # for saving a function as a file
import logging # for changing the tf's logging level


import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras import layers, initializers, losses, optimizers, metrics

import transformers
from transformers import TFBertModel

# 이번 실습에서 추가되었습니다

import sentencepiece as spm
from tokenization_kobert import KoBertTokenizer


data_path = './temp_data/'


# 1) Load the Model-builder function
with open(data_path + 'model_koBERTfunction_v1.pkl', 'rb') as f: # 이번 실습에서 변경되었습니다
    create_model = dill.loads(pickle.load(f)) # use dill to pickle a python function

# 2) Load the Bert-tokenizer
tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')

# 3) Create the model & load the Model-weights (from checkpoint file)
model = create_model(max_length=128)

checkpoint_path = './temp_data/saved_models/'
model.load_weights(filepath=checkpoint_path + 'best_kobert_weights.h5') # 이번 실습에서 변경되었습니다

