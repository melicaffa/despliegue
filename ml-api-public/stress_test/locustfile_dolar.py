import time
import random
from locust import HttpUser, task

class QuickstartUser(HttpUser):

    @task(1)
    def index(self):
        self.client.get('/')

    @task(3)
    def predict(self):
        caso = random.randint(0, 1)
        if caso == 0:
            self.client.post('/predict', params={'text': 'Lindo dia!'})
        elif caso== 1:
            self.client.post('/predict', params={'text': 'Que feo dia'})
        else:
            self.client.post('/predict', params={'text': 'Hola'})
           

    def on_start(self):
        pass
