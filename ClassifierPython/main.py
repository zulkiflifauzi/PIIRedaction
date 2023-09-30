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
warnings.filterwarnings('ignore')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit

@app.route('/upload', methods=["POST"])
def main():  
    requestData = json.loads(request.data) 
    input = requestData['FileName']
    x = requestData['ImageBytes']
    y = base64.b64decode(x)
    with open("file.csv", "wb") as fh:
        fh.write(y)
    #with open("my_file.csv", "wb") as binary_file:   
        # Write bytes to file
        #binary_file.write(x)
    data = {
        "result" : input
    }
    return jsonify(data)
