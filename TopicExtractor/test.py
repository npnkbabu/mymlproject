import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark.sql.functions as sqlfunc
import numpy as np
import pandas as pd

#load a csv

spark = SparkSession.builder.appName('mymlproject').getOrCreate()

df = spark.read.format('csv').load('original.csv',header=True)
df.show()
