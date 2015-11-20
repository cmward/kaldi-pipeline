import glob
import sys
import os
import shutil
from subprocess import call, check_output
from os.path import splitext, abspath, basename
from os.path import join as pjoin
from nltk.corpus import cmudict
from path import *

"""Script to create the lang directory, which includes the dictionary files.
Run this from kaldi-pipeline.

Assumes make_pizza_dir and prepare_pizza_data have been run.
"""

def lexicon(train_text):
    """Create the pronounciation dictionary by getting the cmu dict entry
    for each word in the training text file."""
    pron_dict = cmudict.dict()
    words_seen = set()
    with open(pjoin(PIZZA_LCL_DICT,'lexicon.txt'),'w+') as lexicon:
        with open(train_text) as text:
            for line in text:
                for word in line.split()[1:]:
                    word = word.lower().strip(',.!?')
                    if word not in words_seen:
                        try:
                            prons = pron_dict[word]
                            for pron in prons:
                                lexicon.write(word + ' ' + ' '.join(pron) + '\n')
                        except KeyError:
                            pass #word not in cmudict
                        words_seen.add(word)
        lexicon.write('<UNK> SPN\n')

def non_silence_phones():
    """Create nonsilence_phones, a list of 'real' phones.

    TODO: Put all phones corresponding to base phone on the same line,
    e.g., A A0 A1 A2
    """
    phone_set = set()
    with open('pizza/data/local/dict/nonsilence_phones.txt', 'w+') as nsp:
        with open('pizza/data/local/dict/lexicon.txt') as lexicon:
            for line in lexicon:
                split_line = line.split()[1:] # just get phones
                for phone in split_line:
                    if phone not in phone_set:
                        phone_set.add(phone)
            for phone in phone_set:
                nsp.write(phone+'\n')

def main(data_dir):
    data_dir = abspath(data_dir) # path to data_for_pa3

    # make silence phone files
    silence_phones = pjoin(PIZZA_LCL_DICT, 'silence_phones.txt')
    optional_silence = pjoin(PIZZA_LCL_DICT, 'optional_silence.txt')
    call('echo "SIL" > {}'.format(silence_phones), shell=True)
    call('echo "SIL" > {}'.format(optional_silence), shell=True)

    # make empty 'extra_questions.txt'
    call("touch {}".format(pjoin(PIZZA_LCL_DICT,'extra_questions.txt')),
         shell=True)

    # make the lexicon
    lexicon(pjoin(PIZZA_DATA_TR,'text'))

    # make phone list
    non_silence_phones()

    #Sort files
    files = glob.glob(PIZZA_LCL_DICT+'/*')
    for file in files:
        call("sort {} -o {}".format(file, file),shell=True)

    # use kaldi util to generate the rest of the files
    util_arg = 'utils/prepare_lang.sh {} "<UNK>" {} {}'.format(
                    PIZZA_LCL_DICT, PIZZA_LCL_LANG, PIZZA_LANG)
    call(util_arg, shell=True)

