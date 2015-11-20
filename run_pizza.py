import scripts.make_pizza_dir
import scripts.prepare_pizza_data
import scripts.prepare_pizza_dict
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
    scripts.make_pizza_dir.main(data_dir)
    scripts.prepare_pizza_data.main(data_dir)
    scripts.prepare_pizza_dict.main(data_dir)

if __name__ == "__main__":
    main(sys.argv[1])
