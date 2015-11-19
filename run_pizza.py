import make_pizza_dir
import prepare_pizza_data
import prepare_pizza_dict
import sys
import os
from os.path import abspath
from subprocess import call

"""Main script to process the pizza data. Call from kaldi-pipeline dir.

Usage:
    python run_pizza.py /path/to/data_for_pa3
"""

def main(data_dir):
    data_dir = abspath(data_dir)
    make_pizza_dir.main(data_dir)
    prepare_pizza_data.main(data_dir)
    prepare_pizza_dict.main(data_dir)
    # use kaldi util to generate the rest of the files
    os.chdir('pizza')
    util_arg = ('utils/prepare_lang.sh data/local/dict "<UNK> "' +
                 'data/local/lang data/lang')
    call(util_arg, shell=True)

if __name__ == "__main__":
    main(sys.argv[1])
