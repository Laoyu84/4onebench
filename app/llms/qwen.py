import os
from dotenv import load_dotenv
from openai import OpenAI
from util import constant

load_dotenv()

def launch_client():
    API_KEY = os.getenv('API_KEY')
    if API_KEY is None:
        API_KEY = os.getenv('DASHSCOPE_API_KEY')
    client = OpenAI(
        api_key=API_KEY, 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",   
    )
    return client

def format_messages(sys_msg, user_msg, historicals=None):
    messages = []
    if sys_msg != "":
        messages.append({"role": "system", "content": sys_msg})
    
    if historicals:
        for s in historicals:
            messages.append({"role": s["role"], "content": s["content"]})
    
    if user_msg != "":
        messages.append( {"role": "user", "content": user_msg})   
    #print(f"messages are sent to llms: \n\n {messages}")
    return messages

def completion(
        msgs,
        model = constant.QWENMAX,
        stream = False,
        temperature = 0.05
    ):
    client = launch_client()
    full_response = ""
    completion = client.chat.completions.create(
        model = model,
        messages = msgs,
        temperature = temperature
    )

    if stream:
        for chunk in completion:
            full_response += chunk.choices[0].delta.content
    else: full_response += completion.choices[0].message.content
    return full_response
