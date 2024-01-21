from typing import *
from collections import OrderedDict
from itertools import combinations, combinations_with_replacement as re_combi, product
from functools import reduce
from sys import float_info
FLOAT_EPS = 1E4 * float_info.min

import numpy as np
from scipy import linalg
import pandas as pd
#from matplotlib import pyplot as plt
#plt.rcParams.update({"font.serif": "Times New Roman"})
