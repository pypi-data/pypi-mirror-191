#  Created By Sushil

import torch

gpu = torch.cuda.is_available()
model_type = "t5"
# model_name = "t5-base"
model_name = "t5-small"
model_path = f"outputs/t5-base/trained-epoch-2-train-loss-0.0012-val-loss-0.0011"
# model_path = f"outputs/t5-small/trained-epoch-2-train-loss-0.0039-val-loss-0.0009"
training_csv_path = f"datasets/generated_training.csv"
path_list_data = f"datasets/list_data.csv"
report = "report/%s_test_report.csv" % model_name
un_seen_data = r"datasets/unseen_data.csv"
test_dataset = r"test_dataset/V3-TestCases.csv"
no_of_iteration = 100  # not of iteration to create training data
# training model configuration
max_epochs = 3
num_workers = 2
source_max_token_len = 128
target_max_token_len = 50
outputs = "outputs/%s" % model_name
save_only_last_epoch = True,
batch_size = 8
is_pre_process = False  # Pre process Sentence
is_post_process = True  # Post process Sentence
