#! /usr/bin/env python3
import os
import json
import pathlib
from pprint import pprint
from typing import Dict, Any

# Useful imports for conducting analysis
import numpy as np
import matplotlib.pyplot as plt

# Importing the experiment
from snapshot import *

# List of experiment parameters
# - SHORT_DESCRIPTION
# - HELLO
# - WORLD

PATH = pathlib.Path(__file__).parent.absolute()
DATA_PATH = os.path.join(PATH, 'experiment_data.json')
# Load the all raw data of the experiment
with open(DATA_PATH, mode='r') as json_file:
    DATA: Dict[str, Any] = json.load(json_file)


if __name__ == '__main__':
    print('RAW DATA KEYS:')
    pprint(list(DATA.keys()))

    # The analysis template from the experiment file
    # And we can access all the internal fields of the experiment object
    # and the experiment parameters here!
    print(HELLO, WORLD)
    print(e['strings/hello_world'])
    # logging will print to stdout but not modify the log file
    e.info('analysis done')