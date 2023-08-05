#  Created By Sushil

import config
from custom_t5_model import CustomT5

model = None


def load_model():
    global model
    if model is None:
        model = CustomT5()
        model.load_model(config.model_type, config.model_path, use_gpu=config.gpu)
        model.predict("x can be null")
        print("Model Loaded")
    return model
