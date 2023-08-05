#  Created By Sushil

import pandas as pd

from load_model import load_model
from training_data_creation import create_training_data as createData
from custom_t5_model import CustomT5
from sklearn.model_selection import train_test_split
import os
import config
import util
from util import remove_logDir


def trainModel(df):
    custom_model = CustomT5()
    df.dropna()
    df = df.rename(columns={"UseCase": "target_text", "Sentences": "source_text"})
    df, unseen_df = train_test_split(df, test_size=0.1)
    df = df[['source_text', 'target_text']]
    train_df, test_df = train_test_split(df, test_size=0.20)
    unseen_df = pd.DataFrame(data=unseen_df)
    try:
        os.mkdir("datasets")
    except OSError as error:
        pass
    unseen_df.to_csv(config.un_seen_data, mode='w', index=False)
    print("Test data saved path=%s" % config.un_seen_data)
    print("%s model training started with max_epochs %d and outputDir is %s"
          % (config.model_name, config.max_epochs, config.outputs))
    custom_model.from_pretrained(model_type="t5", model_name=config.model_name)
    custom_model.train(train_df=train_df,
                       eval_df=test_df,
                       source_max_token_len=128,
                       target_max_token_len=50,
                       outputdir=config.outputs,
                       save_only_last_epoch=config.save_only_last_epoch,
                       dataloader_num_workers=int(config.num_workers),
                       batch_size=int(config.batch_size),
                       max_epochs=config.max_epochs, use_gpu=config.gpu)

    remove_logDir()


def predict(sentences):
    sentences = util.pre_processor(sentences)
    # let's load the trained model for inferencing:
    result = load_model().predict(sentences)[0]
    return util.post_processor(result)


def controller(val=0, sentence=""):
    if val == 0:
        use_case = {"UseCase": predict(sentence)}
        print(use_case)
    elif val == 1:
        createData()
    elif val == 2:
        df = pd.read_csv(config.training_csv_path).dropna()
        list_data = pd.read_csv(config.path_list_data).dropna()
        df.update(list_data)
        trainModel(df)
    # elif val == 3:
    #     test.testAccuracy()


if __name__ == '__main__':
    """
    controller(sentence="x is null") It means it will run usecase.
    controller(val=1) It means it will create training dataset.
    controller(val=2) It means it will start training with created dataset.
    controller(val=3) It means it will start Testing accuracy with unseen data.   
    Note: Before running 
    controller(sentence="x is null")
    controller(val=3) 
    Have to change trained model path.
    """
    try:
        load_model()
    except:
        print("Model not found")
    sentence = "Input must be from {10;30}."
    # controller(sentence=sentence)
    controller(1)
    controller(2)
