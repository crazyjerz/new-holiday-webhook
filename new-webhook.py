from concurrent.futures import process
from requests import Session
import json
import re
from datetime import date
from time import sleep
from os import environ
client = Session()
apikeylist = environ['APIKEYLIST'].split(",")
tokenkey = environ['TOKENKEY']
today = str(date.today())
outDict = json.loads(open("outputdict.json", "rt").read())
requestl = []
counter = 0
for code in outDict:
    counter += 1
    request = f"https://holidays.abstractapi.com/v1/?api_key={apikeylist[counter%len(apikeylist)]}&country={code}&year={today[0:4]}&month={today[5:7]}&day={today[8:]}"
    requestl.append(request)
holidays = []
for i in requestl:
    requestedStr = client.get(i).text
    print(requestedStr)
    for i in re.findall('{".*?"}', requestedStr):
        holidays.append(json.loads(i))
    sleep(1)
print(holidays)
holidayList = []
flag = False
for i in holidays:
    for j in holidayList:
        if i['name'] == j['name']:
            j['country'].append(i['country'])
            continue
    if i['name'] not in [j['name'] for j in holidayList]:
        holidayList.append({"name": i['name'], "country": [i['country']]})
print(holidayList)
messageList = []
def sortl(l: list[str]) -> list[str]:
    newl, oldl = [], []
    for i in l:
        if i.find("<@&") == -1:
            newl.append(i)
        else:
            oldl.append(i)
    return newl+oldl
for i in holidayList:
    greeting = "Happy"
    filtered = [{"lgbt", "trans ", "sexual", "gender", "daylight", "robert e. lee"}, {"death", "demise", "assassination", "martyrdom", "ash ", "good friday", "mourning", "catastrophe", "memorial", "fast", "tisha", "kippur", "asarah", "gold star"}]
    for k in filtered[0]: 
        if k in i['name'].lower():
            greeting = ""
            break
    if greeting == "":
        continue
    for j in filtered[1]:
        if j in i['name'].lower():
            greeting = "Have a meaningful"
            break
    roleFragment = "" 
    if len(i['country']) > 10 or ("US" in i['country'] and ("world" in i['name'].lower() or "international" in i['name'].lower())):
        i['country'] = []
    else:
        for g in i["country"]:
            if type(outDict[g]) == int:
                roleFragment += f" <@&{outDict[g]}>"
            else:
                roleFragment += f" {outDict[g]}"
        if roleFragment[-2] == ",":
            roleFragment = roleFragment[:-2]+roleFragment[-1]
    message = f"{greeting} {i['name']}{roleFragment}!"
    print(message)
    messageList.append(message)
messageList = sortl(messageList)
for m in messageList:
    client.post(tokenkey,  data={"wait": 'true', "content": m, "username": "Automated Holiday Announcer"})
    sleep(1)
