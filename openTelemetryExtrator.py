import requests, json
from time import sleep
from flask import Flask,send_file
from time import time
from threading import Thread
import os
import pandas as pd

running = False
current_filename = None

app = Flask(__name__)

def extract(host, serviceName, filename):

    global current_filename
    global running
    current_filename = filename

    data = None
    
    url = host+'/api/v2/traces?serviceName='+serviceName+'&limit=500'
    url = requests.get(url)
    text = url.text
    data = json.loads(text)
    max_time = 0
    organized_data = list()
    while(running):
        organized_data.extend([(data_point[0]['timestamp'],
                                data_point[0]['name'],
                                data_point[0]['tags']['http.method'],
                                data_point[0]['tags']['http.status_code'],
                                data_point[0]['duration']
                                ) for data_point in data if data_point[0]['timestamp'] > max_time])
        
        if max_time < data[0][0]['timestamp']:
            max_time = data[0][0]['timestamp']
            url = host+'/api/v2/traces?serviceName='+serviceName+'&lookback='+str(data[-1][0]['timestamp'])
            url = requests.get(url)
            text = url.text
            data = json.loads(text)
            df = pd.DataFrame(organized_data)
            df.columns = ['Timestamp','Name','Method','Status','Duration']
            df.set_index('Timestamp')
            df.to_csv(filename)
        else:
            sleep(5)
            url = host+'/api/v2/traces?serviceName='+serviceName+'&lookback='+str(data[-1][0]['timestamp'])
            url = requests.get(url)
            text = url.text
            data = json.loads(text)


@app.route('/start')
def start():

    global current_filename
    global running

    running = True
    
    host = os.getenv('HOST')
    serviceName='api'
    filename = str(int(time()))+'.csv'
    current_filename = filename
    extractor = Thread(target=extract,
                        args=(host,serviceName,filename))
    extractor.start()

    return 'Service started'

@app.route('/stop')
def stop():
    global current_filename
    if current_filename != None:
        return send_file(current_filename, download_name=current_filename)
    else:
        return 'Data is not extracted'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='27018')