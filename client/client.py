import socket
from pathlib import Path
import config
import uuid
import inspect
import json


class Client:
    def __init__(self):
        self.comm = SocketCommunicator(config.SERVER_IP, config.SERVER_PORT)

    def sendRequestToServer(self, method, obj):
        id = uuid.uuid4()
        
        success, tries_left = False, config.MSG_MAX_ATTEMPT
        message = [bytes(i) for i in [id, method, obj]]

        while not success and tries_left:
            try:
                
                self.comm.send()
            tries_left -= 1

        
class SocketCommunicator:
    def __init__(self, IP, PORT):
        self.openSocketConnection(IP, PORT)

    def openSocketConnection(self, IP_ADDR, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #todo error handling on fail
        self.socket.settimeout(config.TIMEOUT_MILLISECONDS//1000)
        self.socket.connect(IP_ADDR, PORT)

    def send(self, message: bytes):
        self.socket.sendall(message)
    
    def receive(self):
        return self.socket.recv(config.MESSAGE_MAX_LEN)


class Marshaller:
    @staticmethod
    def marshal(item):
        if inspect.isclass(item):
            item = item.__dict__
        
        return json.dumps(item).encode('utf-8')



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(b"Hello, world")
    #     data = s.recv(1024)

    # print(f"Received {data!r}")
