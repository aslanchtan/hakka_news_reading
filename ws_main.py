import requests
import requests.packages.urllib3
import json
import multiprocessing
import urllib.parse

import websocket
import sys
import wave

import ssl
import threading
import init as initParm

class WebsocketSendData():

    def send_data(slef, websocket, wf):
        print("in send data func")
        buffer_size = int(wf.getframerate() * 0.2)
        websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
        while True:
            data = wf.readframes(buffer_size)
            if len(data) == 0:
                break
            websocket.send_binary(data)

        websocket.send("EOS")


    def getCodeStatus(self, responseData):
        if responseData == "":
            return 0
        responseData = json.loads(responseData)
        codeStatus = responseData['code']
        return str(codeStatus)


    def getWSUrl(self, url, userAccount, userPassword, framerate):
        login_headers = {"Content-Type": "application/json; charset=utf-8"}
        login_account_data = {"username":userAccount,"password":userPassword}
        login_response = requests.post(url + "/api/v1/login", headers=login_headers, json = login_account_data, verify = False)
        json_str = json.dumps(login_response.json())
        json_data = json.loads(json_str)
        login_token = json_data["token"]

        accinfo_token = "Bearer " + login_token
        accinfo_headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": accinfo_token}
        accinfo_response = requests.get(url +"/api/v1/streaming/transcript/access-info", headers=accinfo_headers, verify = False)

        json_str2 = json.dumps(accinfo_response.json())
        accinfo = json_str2.split('"')
        
        enTicket = urllib.parse.quote_plus(accinfo[11])
        wsUrl = accinfo[7]+"?ticket="+enTicket+"&type=raw&rate="+str(int(framerate))
        
        return wsUrl


    def __init__(self, url, userAccount, userPassword, tranFileName):
        super().__init__()

        wf = wave.open(tranFileName, "rb")
        framerate = wf.getframerate()

        wsUrl = self.getWSUrl(url, userAccount, userPassword, framerate)
        ws = websocket.create_connection(wsUrl, sslopt={"cert_reqs": ssl.CERT_NONE})

        while 1:
            message = ws.recv()
            print(message)
            codeStatus = self.getCodeStatus(message)
            if codeStatus == 0:
                break
            print(codeStatus)
            if(codeStatus == "204"):
                print("close ws")
                ws.close()
            
            if(codeStatus == "180"):
                print("send_data")
                thread = threading.Thread(target = self.send_data(ws, wf))
                thread.start()
                thread.join()


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    sys.path.append("init.py")
    url = initParm.webUrl
    userAccount = initParm.account
    userPassword = initParm.password
    threadCount = initParm.threadCount
    tranFileName = initParm.fileName
    print("url = " + str(url))

    workers = []
    for num in range(threadCount):
        workers.append(multiprocessing.Process(target = WebsocketSendData, args = (url, userAccount, userPassword, tranFileName)))
    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()