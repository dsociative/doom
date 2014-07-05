# -*- coding: utf8 -*-
from multiprocessing import Process
from socket_server.base.talker import Talker
from socket_server.client.base_client import BaseClient


class HelloTalkerProcess(Process):

    def __init__(self):
        super(HelloTalkerProcess, self).__init__()
        self.talker = Talker(client_cls=HelloTestClient)

    def run(self):
        self.talker.run()


class HelloTestClient(BaseClient):
    def listen(self, request):
        self.add_resp({'hello': 'world'})

    def disconnect(self, cid):
        pass


if __name__ == '__main__':
    HelloTalkerProcess().run()