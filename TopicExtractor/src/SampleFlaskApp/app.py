from flask import Flask, render_template, Response
from topicsconsumer import TopicsConsumer
import math
import time
import queue
import threading
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def searchTopic():
    return render_template('base.html')

@app.route('/topics', methods=['GET', 'POST'])
def getTopics():
    return render_template('topics.html')

@app.route('/newsandtopics', methods=['GET', 'POST'])
def newsandtopics():
    try:
        def inner():
            newsq = queue.Queue()
            cosumerObj = TopicsConsumer(newsq)
            cosumerObj.startConsumer()
            time.sleep(10)
            while True:
                obj = json.loads(newsq.get())
                # content and topics
                content = json.loads(obj[0])
                topics = obj[1]
                yield '***********************START*********************' + '\r\n' +'News :     ' + '\r\n'   +content['content'] + '\r\n'  + '\r\n' +'Topics :     ' + '\r\n'   +topics +'\r\n'+'***********************END*********************'+ '\r\n'
                time.sleep(10)
        return Response(inner(), mimetype='text/event-stream')
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    app.run(debug=True,port=5050)
