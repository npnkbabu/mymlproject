'''
Data picker : This class picks data from database
'''


import os
import math
from datetime import datetime, timedelta
from utils.database import NewsDatabase
from utils.processor import Processor

class DataPicker(Processor):
    
    def __init__(self):
        print('DataPicker instantiated')
    
    def process(self):
        print('extracting articles data from database')
        return NewsDatabase.getArticlesData()