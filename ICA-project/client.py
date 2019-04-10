# -*- coding: utf-8 -*-


import random

import gevent
import zmq.green as zmq


TIME_OUT = 5000
CLIENT_NUM = 20
CLIENT_BUSY = []
CLIENT_DICT = {}


class Client:
    msg_id = -1

    def __init__(self):
        self.context = zmq.Context()
        self.start_client()

    def client(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, TIME_OUT)
        self.socket.connect('tcp://127.0.0.1:10086')

    def start_client(self):
        client = gevent.spawn(self.client)
        gevent.joinall([client])

    def get_response(self, utterance, client_no):
        self.socket.send_string(utterance)
        reply = self.socket.recv()
        if reply:
            CLIENT_BUSY.remove(int(client_no))
            response = str(reply, encoding="utf-8")
            return response


def load_clients():
    for i in range(CLIENT_NUM):
        CLIENT_DICT[i] = Client()


def select_client():
    i = random.randint(0, 19)
    while True:
        if i == CLIENT_NUM:
            i = 0
        if i in CLIENT_BUSY:
            i += 1
            continue
        else:
            CLIENT_BUSY.append(i)
            # print(CLIENT_BUSY)
            return CLIENT_DICT[i], i

# load_clients()
# cli, index = select_client(each)
# print(cli.get_response(each, index))

