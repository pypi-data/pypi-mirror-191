#  Created By Sushil

import os
import shutil

import config
from operator_enum import Operator


def post_processor(sentence):
    if config.is_post_process:
        for operator in Operator._member_names_:
            sentence = sentence.replace(operator, Operator[operator].value)
    return sentence


def pre_processor(sentence):
    sentence = sentence.replace(".", "")
    if config.is_pre_process:
        for operator in Operator._member_names_:
            sentence = sentence.replace(Operator[operator].value, operator)
    return sentence


def remove_logDir():
    for dir in os.listdir('lightning_logs'):
        shutil.rmtree('lightning_logs/%s' % dir, ignore_errors=True)
