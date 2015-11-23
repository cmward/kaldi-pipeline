import sys
import run_pizza
import glob
import os
from os.path import abspath, basename
from os.path import join as pjoin
from subprocess import call
from scripts.path import *

"""
Usage:
    python run.py /path/to/data_for_pa3
"""
def merge_files(dir1, dir2):
    """dir1 should be where the merged file ends up."""
    dir1 = glob.glob(dir1 + '/*')
    dir2 = glob.glob(dir2 + '/*')
    to_merge = [(file1, file2) for file1 in dir1 for file2 in dir2
                if basename(file1) == basename(file2)]
    for files in to_merge:
        merge_args = "cat {} >> {s} ; sort {s} -u -o {s}".format(
                        files[1], s=files[0])
        call(merge_args, shell=True)

def main(data_dir):
    data_dir = abspath(data_dir)
    os.environ["LC_ALL"] = "C"

    # prepare pizza data and dict
    print "\nPreparing pizza data and dict\n"
    run_pizza.main(data_dir)

    # prepare swbd data and dict
    print "\nPreparing swbd data and dict\n"
    dict_args = "./swbd1_prepare_dict.sh {}".format(data_dir)
    data_tr_args = "./swbd1_data_prep.sh {}".format(pjoin(data_dir, 'train'))
    data_te_args = "./swbd1_data_prep_test.sh {}".format(pjoin(data_dir, 'devtest'))
    call(dict_args, shell=True)
    call(data_te_args, shell=True)
    call(data_tr_args, shell=True)

    # merge generated files
    # the combined files will be in kaldi-pipeline/data
    print "\nMerging pizza and swbd files\n"
    merge_files(TEST, PIZZA_DATA_TE)
    merge_files(TRAIN, PIZZA_DATA_TR)
    merge_files(LCL_DICT, PIZZA_LCL_DICT)

    # prepare_lang.sh using the combined files
    print "\nPreparing combined lang\n"
    call("rm {}".format(pjoin(LCL_LANG, "*")), shell=True)
    call("rm {}".format(pjoin(LCL_DICT, "lexiconp.txt")), shell=True)
    util_arg = 'utils/prepare_lang.sh {} "<UNK>" {} {}'.format(
                    LCL_DICT, LCL_LANG, LANG)
    call(util_arg, shell=True)

if __name__ == "__main__":
    main(sys.argv[1])
