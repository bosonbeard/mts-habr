# send_voice.py - script for sending voice message from MTS EXOLVE

import requests
import csv
import argparse
import json


# Set variables 
# They uses only in send_request function and placed here for easier setup
# Don't forget to paste your MTS EXolve API token and arended phone bellow
token = "Type your API token here" 
arended_phone = "Type here arended MTS exolve phone"
# change this vars if API path will changed
base_url = "https://api.exolve.ru"
urls={
    "send_voice":f"{base_url}/voice-message/v1/MakeVoiceMessage",
    "get_info":f"{base_url}/call/v1/GetInfo",
    "send_sms":f"{base_url}/SendSMS"
    }
head = f"Authorization: Bearer {token}"






def send_voice_messages():
    name = "";
    

    with open(in_filepath, 'r', encoding='utf-8-sig', newline='') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for item in reader:
           text_template = get_text_template(name)
           phone = item[1]
           if (text_template and phone ):
                result = send_request(number=item)
                id = result["modelos"][0]["codigo"] #change to real api
                print(writerow([id, item[0], item[1] ] ))
                print(id)
           else:
               next(reader, None);  # skip the broken record
               print(["Error: not correct data", item[0], item[1] ] )
                
                




def read_csv(in_filepath):
    guests_list =[]
    with open(in_filepath, 'r', encoding='utf-8-sig', newline='') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for item in reader:
            guests_list.append(item)
            else:
                print(["Error: not correct data", item ] )
    return guests_list


def send_request(number):
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos"
    response = requests.request("GET", url)
  
    return response.json()

def send_voice_messages(phones):
    name = "";

def check_listened()


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
    

    with open(in_filepath, 'r', encoding='utf-8-sig', newline='') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for item in reader:
           text_template = get_text_template(name)
           phone = item[1]
           if (text_template and phone ):
                result = send_request(number=item)
                id = result["modelos"][0]["codigo"] #change to real api
                print(writerow([id, item[0], item[1] ] ))
                print(id)
           else:
               next(reader, None);  # skip the broken record
               print(["Error: not correct data", item[0], item[1] ] )



if __name__ == '__main__':
    # parse path to csv file (deault - guest_list.csv.csv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, required=False, default='guest_list.csv.csv')    
    print ("start")
    args = parser.parse_args()

    guests_list= read_csv(args.inpath)
    success_voice_sent,error_voice_sent=send_voice_messages(guests_list)
    listen_list, need_sms_list = check_listened (success_voice_sent)
    success_sms_sent, error_sms_sent = send_sms(need_sms_list)
    print(f"I have {card.price}")
    print(f"I have {card.price}")
    print(f"I have {card.price}")

