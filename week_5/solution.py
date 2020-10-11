import socket
import time


class ClientError(Exception):

    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f'Сервер вернул ответ {self.response}'


class Client:
    response_dict = {}

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        self.status = None
        self.reply = None
        self.response = None

        self.make_connection()

    def make_connection(self):
        try:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
        except socket.timeout as e:
            raise ClientError(f'Connection timeout: {e}')
        except socket.error as e:
            raise ClientError(f'Cannot connect: {e}')

    def process_response(self):
        ans = self.sock.recv(1024).decode("utf8").rstrip()

        self.response = ans.split('\n')
        self.status = self.response[0]
        if self.status != 'ok':
            raise ClientError(self.status)
        if self.reply == '':
            return {}

    def get(self, request):
        self.sock.send(f'get {request}\n'.encode("utf8"))
        self.process_response()

        response_dict = {}
        try:
            self.reply = self.response[1:]
            for item in self.reply:
                key, value, timestamp = item.split()
                if key not in response_dict.keys():
                    response_dict[key] = []
                response_dict[key].append((int(timestamp), float(value)))
                response_dict[key].sort(key=lambda x: x[0])
        except Exception:
            raise ClientError(self.reply)

        return response_dict

    def put(self, name, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        request = f'put {name} {value} {timestamp}\n'.encode('utf8')
        self.sock.send(request)
        self.process_response()
        if self.status == 'error':
            raise ClientError(self.reply)


if __name__ == '__main__':
    c = Client('127.0.0.1', 10001)
    # print(c.get('eardrum.cpu'))
    # print(c.get('get eardrum.cpu\n'))
    # # print(c.get('get lock.cpu\n'))
    # print(c.get('balbalbla'))
    c.put("eardrum.cpu", 27.0, 1000)
    c.put("eardrum.cpu", 27.0, 1001)
    c.put("eardrum.cpu", 27.0, 1002)
    print(c.get('*'))
    c.sock.close()



