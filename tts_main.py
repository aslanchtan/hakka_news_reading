import requests
import requests.packages.urllib3
import urllib3
import multiprocessing
import json
#from urllib.parse import quote
import urllib.parse

import sys
import wave
import os

import ssl
import threading
import init as initParm


class tts():

    def getToken(self, url, username, password):
        login_headers = {"Content-Type": "application/json; charset=utf-8"}
        login_account_data = {"username":username,"password":password}
        login_response = requests.post(url + "/api/v1/login", headers=login_headers, json = login_account_data, verify = False)
        login_token = login_response.json()['token']
        accinfo_token = "Bearer " + login_token
        return accinfo_token

    def getTTSVideo(self, ttsUrl, bearToken, scriptText):
        tts_headers = {'Content-Type': 'application/json','Authorization': bearToken}
        tts_payload = {
            "input": {
            "text": scriptText,
            "type": "common"},
            "voice": {
            "languageCode": "hak-xi-TW",
            "name": "hak-xi-TW-vs2-F01"},
            "audioConfig": {
            "speakingRate": 1
            }}

        ttsResult = requests.post(ttsUrl + "/api/v1/tts/synthesize", headers=tts_headers, json = tts_payload, verify = False)
        return ttsResult

    def saveWaveFile(self, ttsResult, num):
        wav_bytes = ttsResult.content
        wav_path = "tts_result/output" +str(num) + ".wav"
        with open(wav_path, 'wb') as file:
            file.write(wav_bytes)

    def __init__(self, url, username, password, ttsUrl, num, scriptText):
        print("tts_init",str(num))
        # import urllib3
        # requests.packages.urllib3.disable_warnings()

        super().__init__()

        bearToken = self.getToken(url, username, password)
        ttsResult = self.getTTSVideo(ttsUrl, bearToken, scriptText)
        # print(ttsResult.status_code)
        # print(bearToken)
        if ttsResult.status_code == 200:
            self.saveWaveFile(ttsResult, num)
            print("tts_complete",str(num))
        else :
            print("tts_fail",str(num),",resp. code:",str(ttsResult.status_code))

def readTxt(txtName):
    with open(txtName, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.split("\n")
        return content

def tts_api(filepath, threadcount):
    requests.packages.urllib3.disable_warnings()

    transFile = filepath
    threadCount = threadcount
    url = "https://hktts.bronci.com.tw/"
    ttsUrl = "https://hktts.bronci.com.tw/"
    username = "hackathon2025_039"
    password = "!EVuy&4Oq516"

    scriptText = readTxt(transFile)
    print(scriptText)
    threadCount = int(threadCount)

    workers = []
    for num in range(threadCount):
        workers.append(multiprocessing.Process(target = tts, args = (url, username, password, ttsUrl, num, scriptText[num])))

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()



if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    sys.path.append("init.py")
    transFile = initParm.transFile
    threadCount = initParm.threadCount
    url = initParm.webUrl
    ttsUrl = initParm.ttsUrl
    username = initParm.username
    password = initParm.password

    scriptText = readTxt(transFile)
    print(scriptText)
    threadCount = int(threadCount)

    workers = []
    for num in range(threadCount):
        workers.append(multiprocessing.Process(target = tts, args = (url, username, password, ttsUrl, num, scriptText[num])))

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

