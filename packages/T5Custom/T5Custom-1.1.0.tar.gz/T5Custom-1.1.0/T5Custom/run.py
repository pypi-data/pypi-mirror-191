#  Created By Sushil

import time

import pandas as pd
from flask import Flask
from flask_cors import CORS
import controller

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/getPrediction/<string:sentences>/')
def getSentences(sentences):
    start_time = time.time()
    result = controller.predict(sentences)

    running_time = "%s seconds :" % (time.time() - start_time)
    return {"sentences": sentences, "Usecase": result, "execution_time": running_time}


@app.route('/api/train/<string:dataCreation>/')
def train(dataCreation=False):
    controller.train_model(bool(dataCreation))


@app.route('/api/test/<string:csv_path>/')
def test(csv_path=None):
    global df
    if csv_path is not None:
        df = pd.read_csv(csv_path)
    controller.testTrainedModelWithUnseenData(df)
    return "test completed"


app.debug = False
app.run()
