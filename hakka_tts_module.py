# ✅ 修改後的 tts_main.py
import requests
import requests.packages.urllib3
import urllib.parse
import wave
import os
import multiprocessing

requests.packages.urllib3.disable_warnings()

class tts():
    def getToken(self, url, username, password):
        login_headers = {"Content-Type": "application/json; charset=utf-8"}
        login_account_data = {"username": username, "password": password}
        response = requests.post(url + "/api/v1/login", headers=login_headers, json=login_account_data, verify=False)
        token = response.json()['token']
        return "Bearer " + token

    def getTTSVideo(self, ttsUrl, token, scriptText):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }
        payload = {
            "input": {"text": scriptText, "type": "common"},
            "voice": {"languageCode": "hak-xi-TW", "name": "hak-xi-TW-vs2-F01"},
            "audioConfig": {"speakingRate": 1}
        }
        return requests.post(ttsUrl + "/api/v1/tts/synthesize", headers=headers, json=payload, verify=False)

    def saveWaveFile(self, result, filename):
        with open(filename, 'wb') as f:
            f.write(result.content)

    def __init__(self, url, username, password, ttsUrl, filename, scriptText):
        token = self.getToken(url, username, password)
        result = self.getTTSVideo(ttsUrl, token, scriptText)
        if result.status_code == 200:
            self.saveWaveFile(result, filename)
            print(f"🟢 客語 TTS 成功 ({filename})")
        else:
            print(result.status_code)
            print(scriptText)
            print(f"❌ 客語 TTS 失敗（{filename}):{result.status_code}")
            

def generate_hakka_wav(text, index):
    url = "https://hktts.bronci.com.tw/"
    ttsUrl = "https://hktts.bronci.com.tw/"
    username = "hackathon2025_039"
    password = "!EVuy&4Oq516"
    out_path = f"temp_audio/segment_{index}.wav"
    tts(url, username, password, ttsUrl, out_path, text)

# 保留原有 batch 用法

def readTxt(txtName):
    with open(txtName, 'r', encoding='utf-8') as file:
        return file.read().split("\n")

def tts_api(filepath, threadcount):
    transFile = filepath
    url = "https://hktts.bronci.com.tw/"
    ttsUrl = "https://hktts.bronci.com.tw/"
    username = "hackathon2025_039"
    password = "!EVuy&4Oq516"
    scriptText = readTxt(transFile)
    threadCount = int(threadcount)
    workers = []
    for num in range(threadCount):
        out_path = f"tts_result/output{num}.wav"
        workers.append(multiprocessing.Process(target=tts, args=(url, username, password, ttsUrl, out_path, scriptText[num])))
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
