import pycamunda.externaltask
import pycamunda.variable
import pycamunda.processdef
import pycamunda.processinst
import time
import http.client
import json
import datetime

# ssettings

SYSTEM_PHONE = "{your phone}"
COLLECTOR_PHONE = "{collector phone}"
API_KEY = "{API token}"
MESSAGE = "Отправлять машину?"
 
url = 'http://localhost:8080/engine-rest' # Correct port (assuming standard Camunda)
worker_id = 'my-worker'


def get_formatted_timestamp_utc():
    """Generates a timestamp in the format: YYYY-MM-DDTHH:MM:SS.ffffff+00:00 (UTC)."""
    # Get current UTC time
    utc_now = datetime.datetime.utcnow()
    # Format and append the UTC timezone offset
    formatted_timestamp = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f') + '+00:00'
    return formatted_timestamp
 
def send_sms():
  #send sms via MTS Exolve SMS API
  conn = http.client.HTTPSConnection("api.exolve.ru")
  payload = json.dumps({
    "number": SYSTEM_PHONE,
    "destination": COLLECTOR_PHONE,
    "text": MESSAGE
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+API_KEY}
  conn.request("POST", "/messaging/v1/SendSMS", payload, headers)
  res = conn.getresponse()
  return res

def recieve_sms():
  #recieve SMS via MTS Exolve SMS API
  conn = http.client.HTTPSConnection("api.exolve.ru")
  payload = json.dumps({
    "receiver": SYSTEM_PHONE,
    "direction": 1,
    "date_gte": str(sms_date)
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+API_KEY}
  conn.request("POST", "/messaging/v1/GetList", payload, headers)
  res = conn.getresponse()
  return res


# setup Camunda process and topics
start_instance = pycamunda.processdef.StartInstance(url=url, key='sendReceiveSms')
process_instance = start_instance()



fetch_and_lock_sent = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
fetch_and_lock_sent.add_topic(name='send_sms', lock_duration=10000) 

fetch_and_lock_receive = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
fetch_and_lock_receive.add_topic(name='receive_sms', lock_duration=10000) 

# get current timestamp to filter SMS
sms_date= get_formatted_timestamp_utc()

# Wait for process execute first task
time.sleep(5)

# Main loop for Camunda process
while (True):
  try:
      # get task
      tasks_sent = fetch_and_lock_sent()
      if tasks_sent:
          for task in tasks_sent:
            complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
            sms_res = send_sms()
            if (sms_res.status):
              complete.add_variable(name='sent', value=True)
            else:
              complete.add_variable(name='sent', value=False)
            complete()
            print("Send tasks complited")
      else:
        print("No tasks in send SMS block available")
  except Exception as e:
    print(f"An error has occurred: {e}") 

  try:
      # Wait for process execute second task
      time.sleep(20)


      # get task
      tasks_receive = fetch_and_lock_receive()
      if tasks_receive:
          for task in tasks_receive:
            # get opened tasks
            complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)

            #get sms
            sms_res = recieve_sms()

            #get message from response body
            res_json = json.loads(sms_res.read().decode("utf-8"))
            if ("messages" in res_json) and ( len(res_json["messages"])):
              message_text = res_json['messages'][0]['text'].lower().strip()
            else:
              message_text = ""
            if (message_text == "да"):
             # if get approved from sms, go to main flow 
              complete.add_variable(name='need_car', value=True)
            else:
              # if get approved from sms, go to alternative flow 
              complete.add_variable(name='need_car', value=False)
            complete()     
            print("Recieve tasks complited")
      else:
        print("No tasks in recieve SMS block available")
  except Exception as e:
    print(f"An error has occurred: {e}") 

  # Get status of current process
  is_process_active = pycamunda.processinst.GetList(url=url, process_instance_ids=[process_instance.id_], active = True).__call__()
  #End loop if Camunda process finished
  if (not is_process_active):
     print ("Process finished")
     break
