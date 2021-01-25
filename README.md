# MyMLProject
Docker : 
first start docker for postgress, kafka

NewsDataSource:
This project is to extract news data from API.
Its operated in 2 ways
offline : extract news data and store in postgress db
online : start kafka producer

SampleFlaskApp:
its webUI where kafka consumers listens for data and show topics out of that. We start NewsDataSource with online True, so that its kafka producer starts getting data from news API and broadcasts.

 pipeline
1. Feature store : its optional comp to store features so that multiple ML projects can query and get
2. Data extractor : This has 2 modes offline (get data from DB) , online (start kafka consumer)
3. Data analysis (only in Experiment stage)
4. Data validation
5. Data preparation
6. model training
7. model evaluation
8. model validation

# NewsAPI
url : https://newsapi.org/docs/get-started
## Dev account restrictions : 
100 articles in 1 pull
100 pulls in 24hrs

$ pip install newsapi-python
'http://newsapi.org/v2/<endpoint>?<filters>&apiKey=<apikey>'
Usage
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='<news api key>')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/sources
sources = newsapi.get_sources()

endpoint:
top-headlines : for headlines.
everything : articles from over 50,000 large and small news sources and blogs.
sources : returns the subset of news publishers that top headlines (/v2/top-headlines) are available from

filters:
q='bitcoin',
sources='bbc-news,the-verge',
category='business',
language='en',
country='us'

# Process:
first build simple pipelines then extend them with open source tools
Feature store : This should be common for both Experimental and production pipeline. THis is to store features of data to server data scientists. Actually here we store data from different datasources and make it available with API. For example customer average spending per year is calculated from customer data and customer transaction data. so we provide and API to extract customer average spending per year value. please note its not cleaned, ready to work with model data, the main purpose is to extract data from centralized location (feature store) with high thoughtput and low latency real time format or offline bulk extract format with API.
IN our case, we don't use it as we don't have many datasources.

1. Data Extraction : You select and integrate the relevant data from features store sources for the ML task
3. Data analysis (only in Experiment stage) : EDA
4. Data validation : handle data schema skew and data value skews
5. Data preparation : prepare featues suitable for model
6. model training : train model
7. model evaluation : use coherence and make the best model
8. model validation : compare with previous model performance 

# Architecture:
We use docker for components setup and google colab for coding 
There are 2 data sources. one is Postgres container where we take batch data for experimentation.Another data source is Kafka container which will use NEWSAPI to extract data. and this data is production data which will be processed by spark container and provide topics. we execute the code in local maachine so that it will connect to mongo db, kafka and spark containers and process the data. we check for triggering mechanism depeding on model performance.

created postgres and pgadmin container with connected volumes in docker compose.
To restore the newdb_bkup from local to postgres container
a. docker cp <local path/newsdb_bkup>  0c495e1c5bf7:/backups
b. docker exec -it <postgres_container_id> bash
c. pg_restore -U postgres -d newsdb newsdb_bkup
Now once db is regstore it will be automatically mapped to our local volume which is configured in postgres image.

setting spark
install spark 3.0.1 (python 3.8)... spark 2.4.7 supports only upto python 3.7
offline preprocessing and online preprocessing
offline preprocessing : extract data from db and push it to spark

setting kafka container
set kafka from docker-compose and mention topic "KAFKA_CREATE_TOPICS". in order to test it use below procedure
a. set 2 bash terminals from  kakfa container. one for producer and another for consumer
b. enter below command in producer to send a message to "newsfeedtopic" topic (provided you already created "newsfeedtopic" topic from KAFKA_CREATE_TOPICS). It will show ">" waiting for a message
kafka-console-producer.sh --broker-list localhost:9092 --topic test
c. come to consumer terminal and enter below command to start listening 
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test
d. come back to producer terminal and enter a message. which should appear in consumer terminal

Now we need to take "headline" news and send through kafka producer and consumer in datapicker will be waiting for message once received need to run the prediction service.
