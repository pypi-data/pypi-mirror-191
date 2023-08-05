#  Created By Sushil

import os
import time
import config
import pandas as pd
import util
from main import predict


def testAccuracy(unseen_df=None):
    try:
        os.mkdir("report")
    except OSError as error:
        pass
    if unseen_df is None:
        unseen_df = pd.read_csv(config.un_seen_data)
    report = pd.DataFrame(
        data={"classifications": [None], "sentence": [None], "Predicted": [None], "Expected": [None], "Result": [None]})
    for ind in unseen_df.index:
        start = time.time()
        sentence = unseen_df['source_text'][ind]
        target = unseen_df['target_text'][ind]
        use_case = predict(sentence)
        target = util.post_processor(target)
        end = time.time()
        execution_time = (end - start) * 10 ** 3
        print("The time of execution of above program is :%d ms" % execution_time)
        if use_case.casefold().replace("{", "").replace("}", "") != target.casefold():
            df1 = pd.DataFrame(
                data={"classifications": unseen_df['classifications'][ind], "sentence": [sentence],
                      "Predicted": [use_case], "Expected": [target], "Result": ["Fail"],
                      "execution_time(in ms)": execution_time})
        else:
            df1 = pd.DataFrame(
                data={"classifications": unseen_df['classifications'][ind], "sentence": [sentence],
                      "Predicted": [use_case], "Expected": [target], "Result": ["Pass"],
                      "execution_time(in ms)": execution_time})
        if len(report.dropna()) == 0:
            report = df1
        report = pd.concat([report, df1])
        print(ind, "out of", len(unseen_df), ": ", sentence, target, df1["Result"][0])
        report.to_csv(config.report, mode='w', index=False)
    # report.to_csv(config.report, mode='w', index=False)

