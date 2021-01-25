import os
import math
from datetime import datetime, timedelta
from kafka import KafkaConsumer
import threading
import json
import sys
import time
from pprint import pprint
import queue
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class TopicsConsumer:
    def __init__(self,newsq):
        self.consumer = KafkaConsumer('test',\
            bootstrap_servers=['172.18.0.3:9092'],\
            auto_offset_reset='earliest',\
            group_id='consumer-group-a')
        self.newsq = newsq
        today = datetime.today().strftime('%Y-%m-%d')
        dataPrep = os.path.join(DATA_PATH, today,'dataPipeline.pkl')
        modelfile = os.path.join(DATA_PATH, today,'topicmodel.pkl')
        with open(dataPrep,'rb') as plkfile:
            self.prepareData = pickle.load(plkfile)
        with open(modelfile,'rb') as plkfile:
            self.model = pickle.load(plkfile)

    def startConsumer(self):
        self.running = True
        print('starting getting news')
        thrd = threading.Thread(target=self.extractNewsAndTopics)
        thrd.daemon=True
        thrd.start()
        
    def extractNewsAndTopics(self):
        while self.running:
            for msg in self.consumer:
                message = msg.value.decode('utf-8')
                pprint('received ====> {0}'.format(message))
                topics = self.predictSample(message)
                self.newsq.put(json.dumps((message,topics)).encode('utf-8'))

    def predictSample(self,sampleData):
        try:
            tuples = [[1,sampleData]]
            df = pd.DataFrame(tuples,columns=['article_id','content'])
            processedData = self.prepareData.transform(df)
            corpus = processedData[1]
            id2word = processedData[0]
            topics = self.model.print_topics()
            newtopics = self.model[corpus]
            string = ''
            for topic in newtopics:
                for res in topic[0]:
                    string = string + str(res[1]) + '==>' + topics[res[0]][1] + '\r\n'+ '\r\n'
            return string
        
        except Exception as ex:
            print(ex)
    
    def stopconsumer(self):
        self.running = False
    


# if __name__ == '__main__':
#     cosumerObj = TopicsConsumer()
#     cosumerObj.startConsumer()

# input('press any key to stop')