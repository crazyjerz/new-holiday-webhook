from concurrent.futures import process
import httpx
import json
import re
from datetime import date
from time import sleep
from os import environ
client = httpx.Client()
apikeylist = environ['APIKEYLIST'].split(",")
tokenkey = environ['TOKENKEY']
today = str(date.today())
outDict = json.loads(open("outputdict.json", "rt").read())
requestl = []
counter = 0
for code in outDict:
    counter += 1
    request = f"https://holidays.abstractapi.com/v1/?api_key={apikeylist[counter%10]}&country={code}&year={today[0:4]}&month={today[5:7]}&day={today[8:]}"
    requestl.append(request)
holidays = []
for i in requestl:
    requestedStr = client.get(i).text
    for i in re.findall('{".*?"}', requestedStr):
        holidays.append(json.loads(i))
    sleep(0.1)
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
for i in holidayList:
    roleFragment = " "
    if len(i['country']) > 10:
        i['country'] = []
    else:
        for g in i["country"]:
            if type(outDict[g]) == int:
                roleFragment += f" <@&{outDict[g]}> "
            else:
                roleFragment += f"{outDict[g]}"
        if roleFragment[-2] == ",":
            roleFragment = roleFragment[:-2]+roleFragment[-1]
    message = f"Happy {i['name']}{roleFragment.strip()}!"
    print(message)
    client.post(tokenkey,  data={"wait": 'true', "content": message, "username": "Automated Holiday Announcer"})
