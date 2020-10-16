import asyncio


user_data = {}


def make_response(dict_key):
    res = ''
    for value in user_data[dict_key]:
        v_str = ' '.join(list(map(str, value)))
        res += f'{dict_key} {v_str}\n'
    return res


def get_all_entries():
    res = ''
    for key in user_data.keys():
        res += make_response(key)
    return res


def return_get_request(key):
    if key in user_data.keys():
        response = 'ok\n' + make_response(key) + '\n'
    elif key == '*':
        response = 'ok\n' + get_all_entries() + '\n'
    else:
        response = 'ok\n\n'
    return response


def return_put_request(key, request):
    try:
        metric = float(request[2])
        timestamp = int(request[3])
        values = (metric, timestamp)

        if key in user_data.keys():
            for index, item in enumerate(user_data[key]):
                if item[1] == timestamp:
                    user_data[key][index] = values
                    return 'ok\n\n'
            user_data[key].append(values)
        else:
            user_data[key] = [values]
        response = 'ok\n\n'
    except ValueError:
        response = 'error\nwrong command\n\n'
    return response


def parse_request(request):
    try:
        if len(request) > 4:
            return 'error\nwrong command\n\n'
        method = request[0]
        key = request[1]
        if method == 'get' and len(request) == 2:
            response = return_get_request(key)
        elif method == 'put':
            response = return_put_request(key, request)
        else:
            response = 'error\nwrong command\n\n'
        return response
    except IndexError or KeyError or ValueError:
        return 'error\nwrong command\n\n'


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        message = data.decode().strip()
        request = message.split(' ')
        response = parse_request(request)
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)



