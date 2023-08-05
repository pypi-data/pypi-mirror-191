#  Created By Sushil
from load_model import load_model
from main import predict
from main import trainModel
from training_data_creation import create_training_data as createData
from test import testAccuracy
import pandas as pd
import config

model = load_model()


def getPrediction(description):
    return predict(description)


def createNewData():
    createData()


def train_model(with_new_data=True):
    if with_new_data:
        createNewData()
    df = pd.read_csv(config.training_csv_path).dropna()
    list_data = pd.read_csv(config.path_list_data).dropna()
    df.update(list_data)
    trainModel(df)


def testTrainedModelWithUnseenData(df=None):
    testAccuracy(df)
