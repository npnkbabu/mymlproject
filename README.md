# MyMLProject

 pipeline
1. Feature store
2. Data extractor
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
Feature store : This should be common for both Experimental and production pipeline. Take data from NewsAPI and store in postgres. Process it and make features out of it. 
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
create spark container and process preprocessing jobs through spark

setting kafka container
set kafka from docker-compose and mention topic "KAFKA_CREATE_TOPICS". in order to test it use below procedure
a. set 2 bash terminals from  kakfa container. one for producer and another for consumer
b. enter below command in producer to send a message to "test" topic (provided you already created "test" topic from KAFKA_CREATE_TOPICS). It will show ">" waiting for a message
kafka-console-producer.sh --broker-list localhost:9092 --topic test
c. come to consumer terminal and enter below command to start listening 
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test
d. come back to producer terminal and enter a message. which should appear in consumer terminal

Now we need to take "headline" news and send through kafka producer and consumer in datapicker will be waiting for message once received need to run the prediction service.
