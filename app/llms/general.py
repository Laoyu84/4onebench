import os
from llms import zhipu,openai,qwen,doubao
from util import constant
from util.tools import extract_json
from util.logger import logger

def verify_api_key():
    complete("","Hello!")


def complete_verify(sys_msg, usr_msg):
    model = os.getenv('MODEL')
    # use the strongest model to verify routines
    if model in constant.GLM_FAMILY:
        messages = zhipu.format_messages(sys_msg,usr_msg)
        result = extract_json(zhipu.completion(messages, temperature=0.1, model=constant.GLM_VERIFIER))
    elif model in constant.OPENAI_FAMILY:
        messages = openai.format_messages(sys_msg,usr_msg)
        result = extract_json(openai.completion(messages, temperature=0, model=constant.OPENAI_VERIFIER))
    elif model in constant.QWEN_FAMILY:
        messages = qwen.format_messages(sys_msg,usr_msg)
        data_json = qwen.completion(messages, temperature=0, model=constant.QWEN_VERIFIER)
        result = extract_json(data_json)
    elif model in constant.DOUBAO_FAMILY:
        messages = doubao.format_messages(sys_msg,usr_msg)
        data_json = doubao.completion(messages, temperature=0, model=constant.DOUBAO_VERIFIER)
        result = extract_json(data_json)
    return result


def complete(sys_msg, usr_msg):
    model = os.getenv('MODEL')
    if model in constant.GLM_FAMILY:
        messages = zhipu.format_messages(sys_msg,usr_msg)
        result = zhipu.completion(messages, 
                                  model=model,
                                  temperature=0.1)
    elif model in constant.OPENAI_FAMILY:
        messages = openai.format_messages(sys_msg,usr_msg)
        result = openai.completion(messages, 
                                   model= model, 
                                   temperature=0)
    elif model in constant.QWEN_FAMILY:
        messages = qwen.format_messages(sys_msg,usr_msg)
        result = qwen.completion(messages, 
                                model= model, 
                                temperature=0)
    elif model in constant.DOUBAOPRO32K:
        messages = doubao.format_messages(sys_msg,usr_msg)
        result = doubao.completion(messages, 
                                model= model, 
                                temperature=0)
    return result
    