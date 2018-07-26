# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 16:23:45 2018

@author: Korah
"""

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods = ['POST'])
def webhook():
	req = requests.get_json(silent = True, force = True)
	print(json.dumps(req, indent = 4))

	res = makeResponse(req)
	res = json.dumps(res, indent = 4)
	r = make_response(res)
	r.headers ['Content-Type'] = 'application/json'
	return r
	 
def makeResponse(req):
    result = req.get('result')
    parameters = result.get('parameters')
    city = parameters.get('geo-city')
    date = parameters.get('date')
    r = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=' + city + '&appid=68fafa95bd2ae49ca0e0c228c1a8c62b')
    json_object = r.json()
    weather = json_object['list']
    for i in range(0, len(weather)):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break
    
    speech = "The forecast for " + city + "for" + date + " is " + condition
    return {
    "speech" : speech,
    "displaytext" : speech,
    "source" : "apiai-weather-webhook"}
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" %port)
    app.run(debug = False, port = port, host = '0.0.0.0')