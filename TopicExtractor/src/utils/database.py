import psycopg2
import os
import json
import pandas as pd

class NewsDatabase():
    
    def __init__(self):
        print('database instantiated')

    @staticmethod
    def getConnection():
        return psycopg2.connect(
                                        user = os.getenv('MYMLPROJECT_NEWSDB_USER'),
                                        password = os.getenv('MYMLPROJECT_NEWSDB_PASSWORD'),
                                        host = '172.19.0.2',
                                        port = '5432',
                                        database = os.getenv('MYMLPROJECT_NEWSDB_DATABASE'))
    

    @staticmethod
    def dumpSources(sources):
        try:
            connection = NewsDatabase.getConnection()
            cursor = connection.cursor()
            sql = '''TRUNCATE TABLE newsdata.source_details RESTART IDENTITY CASCADE'''
            cursor.execute(sql)
            print('removed {} rows from source_details'.format(cursor.rowcount))
            sql = '''insert into newsdata.source_details (source_id,content) values (%s,%s)'''
            record_to_insert=[]
            for src in sources:
                record_to_insert.append((1,json.dumps(src)))
            cursor.executemany(sql,record_to_insert)
            connection.commit()
            print('{} sources inserted into database'.format(cursor.rowcount))
        except(Exception, psycopg2.Error) as error:
            print('Error connecting to PostgreSQL database', error)
            connection = None
        except:
            print('error occured')
            connection = None
        finally:
            if connection != None:
                cursor.close()
                connection.close()
                print('PostgreSQL connection is now closed')
    
    @staticmethod
    def dumpNewsData(data):
        try:
            connection = NewsDatabase.getConnection()
            cursor = connection.cursor()
            #truncate news_data
            sql = '''TRUNCATE TABLE newsdata.news_data RESTART IDENTITY CASCADE'''
            cursor.execute(sql)
            print('removed {} rows from news_data'.format(cursor.rowcount))

            #truncate article
            sql = '''TRUNCATE TABLE newsdata.article RESTART IDENTITY CASCADE'''
            cursor.execute(sql)
            print('removed {} rows from article'.format(cursor.rowcount))

            sql = '''insert into newsdata.news_data (content) values (%s) RETURNING news_data_id'''
            sqlArticle = '''insert into newsdata.article (news_data_id,content) values (%s,%s)'''
            
            for newsdata in data:
                cursor.execute(sql,(json.dumps(newsdata),))
                news_data_id = cursor.fetchone()[0]
                for article in newsdata:
                    cursor.execute(sqlArticle,(news_data_id,json.dumps(article)))

            connection.commit()
            print('{} news_data inserted into database'.format(cursor.rowcount))
        except(Exception, psycopg2.Error) as error:
            print('Error connecting to PostgreSQL database', error)
            connection = None
        except:
            print('error occured')
            connection = None
        finally:
            if connection != None:
                cursor.close()
                connection.close()
                print('PostgreSQL connection is now closed')

    @staticmethod
    def getArticlesData():
        print('getting articles data')
        try:
            connection = NewsDatabase.getConnection()
            cursor = connection.cursor()
            sqlArticle = '''select article_id,content->>'content' as content from newsdata.article order by article_id '''
            cursor.execute(sqlArticle)
            tuples = cursor.fetchall()
            print('{} articles retrieved'.format(len(tuples)))
            return pd.DataFrame(tuples,columns=['article_id','content'])
            
        except(Exception, psycopg2.Error) as error:
            print('Error connecting to PostgreSQL database', error)
            connection = None
        except:
            print('error occured')
            connection = None
        finally:
            if connection != None:
                cursor.close()
                connection.close()
                print('PostgreSQL connection is now closed')
    
    @staticmethod
    def dumpFeatures(lstData):
        try:
            connection = NewsDatabase.getConnection()
            cursor = connection.cursor()

            #drop existing features
            sql = '''TRUNCATE TABLE newsdata.features RESTART IDENTITY CASCADE'''
            cursor.execute(sql)
            print('removed {} rows from features'.format(cursor.rowcount))

            #store tokens and tfidf into files
            sql = '''insert into newsdata.features (id2word_file,corpus_file,model_file,processeddata_file) values (%s,%s,%s,%s)'''
            cursor.execute(sql,(lstData[0],lstData[1],lstData[2],lstData[3]))
            connection.commit()

            print('{} features inserted into database'.format(cursor.rowcount))
        except(Exception, psycopg2.Error) as error:
            print('Error connecting to PostgreSQL database', error)
            connection = None
        except:
            print('error occured')
            connection = None
        finally:
            if connection != None:
                cursor.close()
                connection.close()
                print('PostgreSQL connection is now closed')
    
    @staticmethod
    def GetFeatures():
        try:
            connection = NewsDatabase.getConnection()
            cursor = connection.cursor()

            #load tokens and tfidf into files
            sql = '''select id2word_file, corpus_file, model_file,processeddata_file from newsdata.features'''
            cursor.execute(sql)
            tuples = cursor.fetchall()
            return [x for x in tuples[0]]
        except(Exception, psycopg2.Error) as error:
            print('Error connecting to PostgreSQL database', error)
            connection = None
        except:
            print('error occured')
            connection = None
        finally:
            if connection != None:
                cursor.close()
                connection.close()
                print('PostgreSQL connection is now closed')
    

