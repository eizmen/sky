import requests
import mysql.connector
import json
import sys
import threading
import datetime
from common import get_headers
from common import get_params
from common import get_iatas
from common import get_request_data
from common import process_data
from common import sem
from common import coll

class Worker(threading.Thread):
    def __init__(self,iata, origen):
        threading.Thread.__init__(self)
        self.data = ""
        self.status = ""
        self.day = origen
        self.iata = iata
        self.fixed_data = {}
        self.connection = coll
        self.semaphore = sem
    def run(self):
        self.make_request()
        if self.status == 200:
            self.fixed_data = process_data(self.data)
            self.insert_mongo()
        else:
            print(self.data)
    def insert_mongo(self):
        self.semaphore.acquire()
        self.connection.insert_many(self.fixed_data)
        self.semaphore.release()
    def make_request(self):
        response = requests.post("https://www.skyscanner.es/g/conductor/v1/fps3/search/", params=get_params(),headers=get_headers(), data=get_request_data(self.day, self.iata))
        self.data, self.status = response.content, response.status_code
        print(self.status)

def get_date():
    start = datetime.datetime.strptime("2020-08-1", "%Y-%m-%d")
    end = datetime.datetime.strptime("2020-08-31", "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days + 1)]
    return date_generated




if __name__ == '__main__':
    iatas = get_iatas()
    for i in iatas:
        for date in get_date():
            day = date.strftime("%Y-%m-%d")
            fixed_iata = i.replace("\n", "")
            worker = Worker(fixed_iata, day)
            worker.start()
        break

    
