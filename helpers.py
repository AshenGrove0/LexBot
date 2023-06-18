import requests
from config import DICT_API_KEY 
import datetime


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_definition(word):
    """Accesses the Marriam webster API to get the definition of a word"""
    base_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    api_key = "?key=" + DICT_API_KEY
	
    print(api_key)
    
    full_api_url = base_url + word + api_key

    try:
        response = requests.get(full_api_url)
        data = json.loads(response.content.decode('utf-8'))[0]
        print(data)
        #Dig through the JSON response to find relevant info
        definition = data['shortdef'][0]
        #Remove text modifiers from raw sentence string
        #print(definition)
        return definition
    except Exception as e:
        print(e)
        return -1