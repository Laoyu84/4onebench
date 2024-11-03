import json

def extract_json(content): 
    if content.find('[') != -1 and content.find(']') != -1:
        return extract_json_array(content)
    else: 
        return extract_json_item(content)

def extract_json_item(content):
    #先验证是否可以被解析
    # Find the index where the list starts and ends
    start_index = content.find('{')
    end_index = content.rfind('}') + 1
    
    # Extract the JSON-like string between these indices
    json_string = content[start_index:end_index]
    print(json_string)
    # Convert the JSON string to a Python list
    json_data = json.loads(json_string)
    
    return json_data

def extract_json_array(content):
    # Find the index where the list starts and ends
    start_index = content.find('[')
    end_index = content.rfind(']') + 1
    
    # Extract the JSON-like string between these indices
    json_string = content[start_index:end_index]
    
    # Convert the JSON string to a Python list
    json_data = json.loads(json_string)
    
    return json_data

