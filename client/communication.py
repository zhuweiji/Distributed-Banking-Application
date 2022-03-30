import socket

from pkg import config
from pkg.comm import marshalling
from pkg.comm import RPCmessages
from pkg.comm import request_types
from pkg.client.logger import log_message


class SocketCommunicator:
    message_count = 0

    def __init__(self):
        # socket_kind = socket.SOCK_DGRAM if use_UDP else socket.SOCK_STREAM
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(config.TIMEOUT_MILLISECONDS//1000)

        self.socket = s

    def sendRequestToServer(self, request, attempts=None):
        if not isinstance(request, request_types.BankingRequest):
            raise ValueError('Request must be a subclass of BankingRequest')

        tries_left = attempts or config.MSG_MAX_ATTEMPT
        success = False

        byte_request = marshalling.marshal(RPCmessages.RPCRequest(request))
        
        while not success and tries_left:
            tries_left -= 1
            response = self._send(config.SERVER_IP, config.SERVER_PORT, byte_request)
            if response:
                return marshalling.unmarshal(response)  
        
        return None

    def recieveFromServer(self):
        response = self._receive()
        if not response:
            return

        return marshalling.unmarshal(response)  
        

    def _send(self, dest_IP, dest_port, message: bytes):
        self.message_count += 1

        addr = (dest_IP, dest_port)
        log_message(f'Sending message to {dest_IP}:{dest_port}. Client tracks this message as number {self.message_count}')
        
        try:
            self.socket.sendto(message, addr)
            response, server = self.socket.recvfrom(1024)
            log_message(f'Received {response} from {dest_IP}:{dest_port}. Client tracks original message as number {self.message_count}')
            return response

        except socket.timeout:
            log_message(f'No response from {dest_IP}:{dest_port}. Client tracks original message as number {self.message_count}')
            return None
    
    def _receive(self):
        try:
            return self.socket.recvfrom(config.MESSAGE_MAX_LEN)
        except socket.timeout:
            return None
        

if __name__ == "__main__":
    s = SocketCommunicator()
    obj = request_types.QueryAccountRequest(1, 'password')
    r = s.sendRequestToServer(obj)
    print(r)
    


# for pings in range(10):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     client_socket.settimeout(1.0)
#     message = b'test'
#     addr = ("127.0.0.1", 12000)

#     start = time.time()
#     client_socket.sendto(message, addr)
#     try:
#         data, server = client_socket.recvfrom(1024)
#         end = time.time()
#         elapsed = end - start
#         print(f'{data} {pings} {elapsed}')
#     except socket.timeout:
#         print('REQUEST TIMED OUT')


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(b"Hello, world")
    #     data = s.recv(1024)

    # print(f"Received {data!r}")
