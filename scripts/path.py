import os
from os.path import join as pjoin

PROJECT_ROOT = os.curdir
PIZZA_DIR = pjoin(PROJECT_ROOT, 'pizza')
PIZZA_WAV_TR = pjoin(PIZZA_DIR, 'train_pizza_audio')
PIZZA_WAV_TE = pjoin(PIZZA_DIR, 'test_pizza_audio')
PIZZA_DATA = pjoin(PIZZA_DIR, 'data')
PIZZA_LANG = pjoin(PIZZA_DATA, 'lang')
PIZZA_LOCAL = pjoin(PIZZA_DATA, 'local')
PIZZA_DATA_TE = pjoin(PIZZA_DATA, 'test_pizza')
PIZZA_DATA_TR = pjoin(PIZZA_DATA, 'train_data')
PIZZA_LCL_DICT = pjoin(PIZZA_LOCAL, 'dict')
PIZZA_LCL_LANG = pjoin(PIZZA_LOCAL, 'lang')