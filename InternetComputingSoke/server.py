# -*- coding: utf-8 -*-

import gevent
import zmq.green as zmq
from whoosh.index import open_dir

from function01 import search_index, connect_db


# agent = control.Agent()
context = zmq.Context()

INDEX_DIR = "indexdir"

def server():
    print("start listening ......")
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.LINGER, 5000)
    socket.bind('tcp://127.0.0.1:10086')
    global INDEX_DIR
    ix = open_dir(INDEX_DIR)
    de_db = connect_db('temporary_comment')
    while True:
        msg = socket.recv()
        msg = str(msg, encoding="utf-8")
        reply = search_index(msg, ix, de_db)
        socket.send_string(reply)  # fixing for recv-send pair

publisher = gevent.spawn(server)
gevent.joinall([publisher])


