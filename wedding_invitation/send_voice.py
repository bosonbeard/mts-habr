# send_voice.py - script for sending voice message from MTS EXOLVE

import requests
import csv
import argparse
import json
import time


# Set variables 
# They uses only in send_request function and placed here for easier setup
# Don't forget to paste your MTS EXolve API token, arended phone, and message id bellow
token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJRV05sMENiTXY1SHZSV29CVUpkWjVNQURXSFVDS0NWODRlNGMzbEQtVHA0In0.eyJleHAiOjIwMjA4MDAyMjcsImlhdCI6MTcwNTQ0MDIyNywianRpIjoiNGY0NmQ2ZjItM2ZmMS00MzIxLWJhY2YtZmEwMTM2NjA5Zjk4IiwiaXNzIjoiaHR0cHM6Ly9zc28uZXhvbHZlLnJ1L3JlYWxtcy9FeG9sdmUiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiOGUwNDRkMTEtNTgxOS00MDk3LWFmNDMtN2RjNjk3MDI2ZWFiIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZmFiYmJlNGItOTE3ZC00ZjVjLTg1ZGUtYWRhZDZkODMzMzAyIiwic2Vzc2lvbl9zdGF0ZSI6ImY0Zjc3NDk0LTI3NDAtNGU0YS1hNDlkLTM4ZDE0ZDg2NTQzNSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1leG9sdmUiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJleG9sdmVfYXBwIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJmNGY3NzQ5NC0yNzQwLTRlNGEtYTQ5ZC0zOGQxNGQ4NjU0MzUiLCJ1c2VyX3V1aWQiOiJkNDRkMDQ1MS03NTFhLTQyNTQtOTFkNC0xMzY4MTQyNzQ3MzUiLCJjbGllbnRJZCI6ImZhYmJiZTRiLTkxN2QtNGY1Yy04NWRlLWFkYWQ2ZDgzMzMwMiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjE3Mi4yMC4yLjIyIiwiYXBpX2tleSI6dHJ1ZSwiYXBpZm9uaWNhX3NpZCI6ImZhYmJiZTRiLTkxN2QtNGY1Yy04NWRlLWFkYWQ2ZDgzMzMwMiIsImJpbGxpbmdfbnVtYmVyIjoiMTIxMDQyMyIsImFwaWZvbmljYV90b2tlbiI6ImF1dGFhMWI0OTI1LWIyZTQtNDY3OC1iNWIzLWMyZDVjMGM1N2QyZSIsInByZWZlcnJlZF91c2VybmFtZSI6InNlcnZpY2UtYWNjb3VudC1mYWJiYmU0Yi05MTdkLTRmNWMtODVkZS1hZGFkNmQ4MzMzMDIiLCJjdXN0b21lcl9pZCI6IjMxMzAwIiwiY2xpZW50QWRkcmVzcyI6IjE3Mi4yMC4yLjIyIn0.NZeIiHICarz0i4C7q26t5q94BCvKAwFwJDCZaaHKTSu-OL788KD8Ach-Xe_s5gUpQbMBkXhsySiHgRMF3j6TBaHVWPYO9rQ7rzYpv6IGzbJy1WVNc3uwdLdLgcEk0hWhNfzj3CHiri4YAHz5FZEVu1yzjuyFHmET2jh6hi6Zveh4qp04zRSr-IBF0X2o4ScrDTvwTCaII_joSvqwewiF-G1OUgoluBch0wK8eUIqluWR_XScoOA5PQfKkw8xZqrntgkEC_7E551RHK7QFGP73wdyxuQFk4Avu7WaFtIuaBGbVgFElI9agLDFNjtjSiZlVOW0gOy6kMFY4Geu_-1d4g' 
arended_phone = "79846650499"
message_id="78987f5b-c281-4d23-be2b-fb7a0402126d"
# change this vars if API path will changed
base_url = "https://api.exolve.ru"
urls={
    "send_voice":f"{base_url}/call/v1/MakeVoiceMessage",
    "get_info":f"{base_url}/call/v1/GetInfo",
    "send_sms":f"{base_url}/messaging/v1/SendSMS"
    }
headers = {
    "Content-Type": "application/json", 
    "Authorization": f"Bearer {token}"
}





def read_csv(in_filepath):
    """
    Read data from csv with columns [id, name, phone] \r \n
    in_filepath - path to csv \r \n
    """
    guests_list =[]
    with open(in_filepath, 'r', encoding='utf-8-sig', newline='') as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for item in reader:
            if (item[0], item[2]):
                guests_list.append(item)
            else:
                print(["Error: not correct data", item ] )
    return guests_list


def send_request(type,body):
    """
    Sending request to MTS Exolve Api \r \n
    type - api method for request (see urls keys above) \r \n
    body - payload for POST method
    """
    result="";
    if type in urls:
        url = urls[type]
        payload = json.dumps(body)
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
    else:
        print("Unknown request type")
    return result

def send_voice_messages(guests_list):
    """
    Sending voice messages by MTS Exolve Api \r \n
    guests_list - list with next structure [id, name, phone] \r \n
    """
    success_voice_list = [];
    error_voice_list = [];
    for guest in guests_list:
        body = {
            "source": f"{arended_phone}",
            "destination": f"{guest[2]}",
            "service_id": f"{message_id}"
        }
        result= send_request("send_voice",body)
        if ( "call_id" in result):
            success_voice_list.append([guest[0],result["call_id"]])
        else:
            error_voice_list.append(guest)
    return success_voice_list, error_voice_list

def check_listened(success_voice_list):
    """
    Checking status of voice messages by MTS Exolve Api \r \n 
    success_voice_list - list of previous success sended voice messages \r \n
    """
    listen_list  = [];
    need_sms_list = [];
    for voice in success_voice_list:
        body = {
            "call_id": f"{voice[1]}"
        }
        result= send_request("send_voice",body)
        if ( "status" in result): 
            if  send_request["status"]=="completed":
                listen_list.append(voice[0])
        else:
            need_sms_list.append(voice[0])
    return listen_list, need_sms_list

def send_sms(guests_list, need_sms_list):
    """
    Sending SMS by MTS Exolve Api \r \n
    guests_list - list with next structure [id, name, phone] \r \n
    need_sms_list - list with ids guests whom we will sent SMS \r \n
    """
    success_sms_list = [];
    error_sms_list = [];
    for guest in guests_list:
        for id in need_sms_list:
            if int(guest[0]) == int(id):
                body = {
                    "number": f"{arended_phone}",
                    "destination": f"{guest[2]}",
                    "text": f"{guest[1]} ждем на нашу свадьбу! Таня + Володя"
                }
                result= send_request("send_sms",body)
                if ( "message_id" in result):
                    success_sms_list.append(guest)
                else:
                    error_sms_list.append(guest)
                break
    return success_sms_list, error_sms_list

if __name__ == '__main__':
    # parse path to csv file (deault - guest_list.csv.csv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, required=False, default='guest_list.csv')    
    print ("start")
    args = parser.parse_args()
    # read csv
    guests_list= read_csv(args.inpath)
    # send voice
    success_voice_list,error_voice_list=send_voice_messages(guests_list)
    # Pause 10 seconds
    time.sleep(30)    
    # Checking who listened voice message
    listen_list, need_sms_list = check_listened (success_voice_list)
    # send SMS for guests whom not listened voice message
    success_sms_list, error_sms_list = send_sms(guests_list, need_sms_list)
    # print results
    print (f"Всего приглашено {(len(success_sms_list)+len(listen_list))} гостей")
    print (f"Не смогли пригласить:", [*error_voice_list, *error_sms_list] )


