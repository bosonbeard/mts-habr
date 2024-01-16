# send_voice.py - script for sending voice message from MTS EXOLVE

import requests
import csv
import argparse
import json


# Set variables 
token = "MTT_TOKEN"
base_url = "https://api.exolve.ru/voice-message/v1"
urls={
    "sendSMS":"{base_url}/SendSMS",
    "sendVoice":"{base_url}/MakeVoiceMessage",
    }

head = f"Authorization: Bearer {token}"

def get_text_template(name):
   
    search_name =name.lover().trim()
    if name():
        if search_name.find(" и ") or search_name.find(","):
          template = f"Дорогие {name}, приглашаем вас к нам свадьбу 01.01.2024! Ждем вас с нетерпением, ваши Иван да Марья"
        else:
           template = f"{name}, приглашаю Вас к нам свадьбу 01.01.2024! Ждем с нетерпением, Иван да Марья"
    
    return template



def send_messages(in_filepath):
    pass

def send_voive_vessage(in_filepath):
    '''
    pip install requests
    python send_voice.py --inpath "/path/to/csv/dataset" --outpath "/path/to/csv/wqithr_results"
    send csv file  (--inpath)
    :return: None
    '''
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
                
                



def send_request(number):
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos"
    response = requests.request("GET", url)
  
    return response.json()




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, required=False, default='guest_list.csv.csv')    
    print ("start")
    args = parser.parse_args()
    voive_vessage(args.inpath,args.outpath)


