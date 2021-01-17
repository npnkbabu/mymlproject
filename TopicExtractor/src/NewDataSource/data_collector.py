'''
Data collector : This class connects NewsAPI collects bulk collection of news articles and insert into db
'''

import os
import math
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from utils.database import NewsDatabase
from utils.newspipeline import NewsPipeline
import threading
from kafka import KafkaProducer, KafkaConsumer
import json
import time
from pprint import pprint

class DataCollector(NewsPipeline):
    def __init__(self):
        print('DataCollector instatiated')

    def process(self):
        try:
            self.key = os.getenv('MYMLPROJECT_NEWS_API_KEY')
            if self.key is None:
                print('Not able to extract news_api key')
                return
            self.newsapi = NewsApiClient(self.key)
            if self.__storeSources():
                self.__storeOfflineArticles()
            return True
        except Exception as ex:
            print('error occured in process : {}'.format(ex))
            return False
    
    def __startKafkaConsumer(self):
        print('starting kafka consumer')
        consumer = KafkaConsumer(self.config['kafka']['topicname'],\
            bootstrap_servers=[self.config['kafka']['server:port']],\
            auto_offset_reset='earliest',\
            group_id='consumer-group-a')

        while True:
            for msg in consumer:
                pprint('received ====> {0}'.format(msg.value.decode('utf-8')))


    def json_serializer(self,data):
        return json.dumps(data).encode('utf-8')

    def json_deserializer(self,data):
        return json.loads(data).decode('utf-8')

    def __startKafkaProducer(self):
        print('starting kafka producer with headlines')
        producer = KafkaProducer(bootstrap_servers=[self.config['kafka']['server:port']]\
            ,value_serializer=self.json_serializer)
        data = self.__getHeadlines()
        
        while True:
            for x in data:
                producer.send(self.config['kafka']['topicname'],x)
                pprint('sent ====> {0}'.format(x))
                time.sleep(10)

    def __getHeadlines(self):
        #return ['test1','test2']
        response = self.newsapi.get_top_headlines(sources='abc-news',language='en')
        if response['status'] == 'ok':
            return response['articles']
    
    def __storeSources(self):
        srcResponse = self.newsapi.get_sources()
        if (srcResponse['status'] == 'ok'):
            NewsDatabase.dumpSources(srcResponse['sources'])
            return True
        else:
            print('unable to extract sources')
            return False
    
    '''
    This function gets all articles available and store them in postgress db.
    for dev account we can get max 100 articles
    '''
    def __storeOfflineArticles(self):
        try:
            print('Storing all articles')
            pageSize = 100
            total_days = 25
            today = datetime.today()
            to_date = today
            from_date = today - timedelta(days=total_days)
            from_date = from_date
            print('Extracting news for {2} days from {0} to {1})'.format(from_date,to_date,total_days))
            articlesList = []
            for date in [from_date + timedelta(n) for n in range(total_days)]:
                extract_date = date.strftime('%Y-%m-%d')
                print('extracting news for {}',date)
                all_articles = self.newsapi.get_everything(
                                            sources='abc-news',
                                            from_param=extract_date,
                                            to=extract_date,
                                            language='en',
                                            sort_by='relevancy',page_size=pageSize)
                if all_articles['status'] == 'ok':
                    articlesList.append(all_articles['articles'])
                    #got 100 articles. store them in postgress and process in next module
                else:
                    print('error while getting news for {}'.format(extract_date))
            if len(articlesList) > 0 :
                NewsDatabase.dumpNewsData(articlesList)
            return True
        
        except Exception as ex:
            print(ex)
            return False
