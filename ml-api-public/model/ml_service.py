# -*- coding: utf-8 -*-
import redis
import json
import time
from classifier import SentimentClassifier

db = redis.Redis(host='redis', port=6379,db=0)

model =  SentimentClassifier()
def sentiment_from_score(score):
    sentiment = None

    if score > 0.55:
        sentiment = 'Positivo'
    elif score < 0.45:
        sentiment = 'Negativo'
    else:
        sentiment = 'Neutral'
    return sentiment


def predict(text):
    sentiment = None
    score = None
    score = model.predict(text)
    sentiment = sentiment_from_score(score)
    return sentiment, score


def classify_process():
 while True:
    queue = db.lrange('service_queue',0,9)
    for q in queue:
        q = json.loads(q.decode('utf-8'))
        job_id = q['text']
        sentiment, score = predict(q['text'])
        response = {'prediction':sentiment, 'score': score}
        db.set(job_id,json.dumps(response))
        
    db.ltrim('service_queue',len(queue), -1)
    time.sleep(1)

if __name__ == "__main__":
    print('Launching ML service...')
    classify_process()
