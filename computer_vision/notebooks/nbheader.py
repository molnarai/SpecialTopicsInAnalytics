%load_ext autoreload
%autoreload 2

import os
import json
import cv2
import matplotlib.pyplot as plt
from helper import (
    imshow,
    load_and_scale,
    load_annotations,
)

DATAPATH = "/data/project/MSA8395/mapillary_traffic_sign_dataset/"
