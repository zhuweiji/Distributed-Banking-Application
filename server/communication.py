import socket

from pkg import config
from pkg.comm import marshalling
from pkg.comm import RPCmessages 
from pkg.comm import request_types
from pkg.server.logger import log_message


class SocketCommunicator:
    def __init__(self, IP=None, PORT=None):
        IP = IP or socket.gethostbyname(socket.gethostname())
        PORT = PORT or config.SERVER_PORT
        log_message(f'Opening socket on {IP}:{PORT}')

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((config.SERVER_IP, config.SERVER_PORT))
        self.socket = server_socket

        self.outgoing_queue = []
        

    def receive_from_client(self):
        request = self._receive_one()
        if not request:
            return 
        
        return marshalling.unmarshal(request)  

    
    def _receive_one(self, *args, **kwargs):
        try:
            message, address = self.socket.recvfrom(1024)
            log_message(f'Received message from {address}')

            ResponseMessage = RPCmessages.RPCResponse(RPCmessages.OK)
            byte_response = marshalling.marshal(ResponseMessage)
            ip, port = address
            self._send(ip, port, message=byte_response)
            return message

        except socket.timeout:
            return None

    def _send(self, dest_IP, dest_port, message: bytes):
        addr = (dest_IP, dest_port)
        self.socket.sendto(message, addr)


    def listen_forever(self):
        while True:
            self._receive_one()




if __name__ == "__main__":    
    # import sys
    # import inspect
    # clsname_boundname_map = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))
    # print(clsname_boundname_map)

    s = SocketCommunicator()
    s.receive_from_client()
    
