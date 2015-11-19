import os
import sys
import shutil
import glob
from os.path import abspath, basename

"""Script to create the directory structure for the pizza data.
Copies the audio files.

Usage:
    python make_pizza_dir.py /path/to/data_for_pa3

Call this from kaldi-pipeline directory.
"""

def make_dir_structure(data_dir):
    """Call this kaldi-pipeline directory. Makes the pizza directory.
    Input is path to data_for_pa3 folder."""
    data_dir = abspath(data_dir)
    try:
        os.mkdir(abspath('.') + "/pizza")
        os.chdir('pizza')
        os.mkdir('test_pizza_audio')
        os.mkdir('train_pizza_audio')
        os.mkdir('data')
        os.chdir('data')
        os.mkdir('test_pizza')
        os.mkdir('train_pizza')
        os.mkdir('lang')
        os.mkdir('local')
        os.chdir('local')
        os.mkdir('dict')
        os.mkdir('lang')
        os.chdir('..')

        # Copy data from data_for_pa3 to pizza directory
        os.chdir('..') # cd up to pizza dir
        # Copy devtest audio files
        for audio_file in glob.glob(data_dir+'/devtest/pizza/*.wav'):
            shutil.copy(
                    audio_file,
                    abspath('test_pizza_audio')+'/'+basename(audio_file))
        # Copy train audio files
        for audio_file in glob.glob(data_dir+'/train/pizza/*.wav'):
            shutil.copy(
                    audio_file,
                    abspath('train_pizza_audio')+'/'+basename(audio_file))
        # Copy kaldi utils to pizza dir
        shutil.copytree('../steps', 'steps')
        shutil.copytree('../utils', 'utils')
    except OSError: # Directory structure has already been created
        print "Pizza directory has already been created."


data_dir = abspath(sys.argv[1])
make_dir_structure(data_dir)
