# send_voice.py - script for sending voice message from MTS EXOLVE

import requests
import csv
import argparse
import json


# Set variables 
# They uses only in send_request function and placed here for easier setup
# Don't forget to paste your MTS EXolve API token and arended phone bellow
token = 'Type here arended MTS exolve phone' 
arended_phone = "Type here arended MTS exolve phone"
# change this vars if API path will changed
base_url = "https://api.exolve.ru"
urls={
    "send_voice":f"{base_url}/voice-message/v1/MakeVoiceMessage",
    "get_info":f"{base_url}/call/v1/GetInfo",
    "send_sms":f"{base_url}/SendSMS"
    }
headers = {
    "Content-Type": "application/json", 
    "Authorization": f"Bearer {token}"
}





def read_csv(in_filepath):
    guests_list =[]
    with open(in_filepath, 'r', encoding='utf-8-sig', newline='') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for item in reader:
            if (item[0], item[1]):
                guests_list.append(item)
            else:
                print(["Error: not correct data", item ] )
    return guests_list


def send_request(type,body):
    result="";
    if type in urls:
        url = urls[type]
        payload = json.dumps(body)
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        print(response.text)
    else:
        print("Unknown request type")
    return result





def send_voice_messages(guests_list):
    name = "";

def check_listened():
    pass

def send_sms(in_filepath):
    template = f"Дорогие {name}, приглашаем вас к нам свадьбу 01.01.2024! Ждем вас с нетерпением, ваши Иван да Марья"

"""
123456
def returnMatches(a, b):
    matches = []
    for i in a:
        if i in b:
            matches.append(i)
    return matches
"""
    

if __name__ == '__main__':
    # parse path to csv file (deault - guest_list.csv.csv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, required=False, default='guest_list.csv')    
    print ("start")
    args = parser.parse_args()

    guests_list= read_csv(args.inpath)
   # print (guests_list)
    send_request("get_info",{"call_id": "caldf32f642-6313-4dae-94db-98502ad3249c"})
  #  success_voice_sent,error_voice_sent=send_voice_messages(guests_list)
  #  listen_list, need_sms_list = check_listened (success_voice_sent)
  #  success_sms_sent, error_sms_sent = send_sms(need_sms_list)
    print(f"I have {guests_list}")
    print(f"I have {guests_list}")
    print(f"I have {guests_list}")

