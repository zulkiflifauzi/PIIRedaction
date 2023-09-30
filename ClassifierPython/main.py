import base64
import requests
from flask import Flask
from flask import request, json, jsonify
import json
app = Flask(__name__)
from json import JSONEncoder
import json
import warnings
import os
import pandas as pd
import train
import asyncio
import client
warnings.filterwarnings('ignore')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit

@app.route('/upload', methods=["POST"])
def main():  
    requestData = json.loads(request.data) 
    input = requestData['FileName']
    x = requestData['Base64string']
    d = base64.b64decode(x)
    with open(input, "wb") as fh:
        fh.write(d)
    print("message: save file complete")
    df = pd.read_csv(input)
    data = {
        "result" : df.columns.to_list()
    }
    return jsonify(data)
@app.route('/testsentence', methods=["POST"])
def testsentence():  
    requestData = json.loads(request.data) 
    fileName = requestData['FileName']
    sentence = requestData['Sentence']
    testSentence = requestData['TestSentence']
    testResult = client.test(fileName, sentence, testSentence)
    data = {
        "Result" : testResult[0].tolist()
    }
    return jsonify(data)

@app.route('/train', methods=["POST"])
async def training():  
    requestData = json.loads(request.data) 
    fileName = requestData['FileName']
    sentence = requestData['Sentence']
    labels = requestData['Labels']
    asyncio.ensure_future(train.train_data(fileName, sentence, labels))  # fire and forget async_foo()
    data = {
        "message" : "Training is in progress."
    }
    return jsonify(data)

if __name__ == '__training__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(training())
