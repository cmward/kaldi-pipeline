import os
import sys
import shutil
import glob
from os.path import abspath, basename
from os.path import join as pjoin
from path import *

"""Script to create the directory structure for the pizza data.
Copies the audio files.

Call this from kaldi-pipeline directory.
"""

def make_dir_structure(data_dir):
    """Call this from kaldi-pipeline directory. Makes the pizza directory.
    Input is path to data_for_pa3 folder."""
    data_dir = abspath(data_dir)
    try:
        os.makedirs(PIZZA_DIR)
        os.makedirs(PIZZA_WAV_TR)
        os.makedirs(PIZZA_WAV_TE)
        os.makedirs(PIZZA_DATA)
        os.makedirs(PIZZA_LANG)
        os.makedirs(PIZZA_LOCAL)
        os.makedirs(PIZZA_DATA_TE)
        os.makedirs(PIZZA_DATA_TR)
        os.makedirs(PIZZA_LCL_DICT)
        os.makedirs(PIZZA_LCL_LANG)
        # Copy data from data_for_pa3 to pizza directory
        # Copy devtest audio files
        for audio_file in glob.glob(data_dir+'/devtest/pizza/*.wav'):
            shutil.copy(
                    audio_file,
                    pjoin(PIZZA_WAV_TE, basename(audio_file))) 
        # Copy train audio files
        for audio_file in glob.glob(data_dir+'/train/pizza/*.wav'):
            shutil.copy(
                    audio_file,
                    pjoin(PIZZA_WAV_TR, basename(audio_file)))
        # Copy kaldi utils to pizza dir
        shutil.copytree(pjoin(PROJECT_ROOT,'utils'),pjoin(PIZZA_DIR,'utils'))
        shutil.copytree(pjoin(PROJECT_ROOT,'steps'),pjoin(PIZZA_DIR,'steps'))
    except OSError: # Directory structure has already been created
        print "Pizza directory has already been created."

def main(data_dir):
    data_dir = abspath(data_dir)
    make_dir_structure(data_dir)
