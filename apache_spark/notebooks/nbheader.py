%reload_ext autoreload
%autoreload 2

from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F
from pyspark.sql.functions import col as S
from pyspark.sql import DataFrame, Row, Window
import os
import sys
import json
import datetime
import re
import pandas as pd
import numpy as np

# spark = SparkSession.builder.master("local[4]").getOrCreate()
# spark.getActiveSession()
# spark.stop()

