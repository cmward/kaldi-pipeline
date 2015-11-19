import glob
import sys
import os
import shutil
from subprocess import call, check_output
from os.path import splitext, abspath, basename
from nltk.corpus import cmudict

"""Script to create the lang directory, which includes the dictionary files.
Run this from kaldi-pipeline.

Assumes make_pizza_dir and prepare_pizza_data have been run.
"""

KALDI_PATH = os.environ['KALDI']

def lexicon(train_text):
    """Create the pronounciation dictionary by getting the cmu dict entry
    for each word in the training text file."""
    pron_dict = cmudict.dict()
    words_seen = set()
    with open('pizza/data/local/dict/lexicon.txt', 'w+') as lexicon:
        with open('pizza/data/train_pizza/text') as text:
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

def non_silence_phones():
    """Create nonsilence_phones, a list of 'real' phones."""
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
    call('echo "SIL" > pizza/data/local/dict/silence_phones.txt', shell=True)
    call('echo "SIL" > pizza/data/local/dict/optional_silence.txt', shell=True)

    # make empty 'extra_questions.txt'
    call("touch pizza/data/local/dict/extra_questions.txt", shell=True)

    # make the lexicon
    lexicon('pizza/data/train_pizza/text')

    # make phone list
    non_silence_phones()

