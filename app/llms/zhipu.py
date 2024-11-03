import os
from dotenv import load_dotenv
from util import constant
from zhipuai import ZhipuAI
from util.logger import logger

load_dotenv()

def launch_client():
    API_KEY = os.getenv('API_KEY')
    if API_KEY is None:
        API_KEY = os.getenv('GLM_API_KEY')
    client = ZhipuAI(api_key= API_KEY)
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
        model = constant.GLM4PLUS,
        stream = False,
        temperature = 0.05
    ):

    
    client = launch_client()
    full_response = ""
    logger.debug(msgs)
    response = client.chat.completions.create(
        model=model,  # 填写需要调用的模型名称
        messages=msgs,
        stream=stream,
        max_tokens = 8192,
        temperature=temperature,
        tools=[{"type": "web_search", "web_search": {"enable": False}}]
    )
    if stream:
        for chunk in response:
            full_response += chunk.choices[0].delta
    else:
        full_response += response.choices[0].message.content
    
    return full_response

def get_embeddings(s):
    client = launch_client()
    response = client.embeddings.create(
        model=constant.EMBEDDING, #填写需要调用的模型名称
        input=s,
    )
    return response.data[0].embedding

