# -*- coding: utf8 -*-
from socket_server.client.simple_client import SimpleClient
from doom.executor import Executor


class ExecutorClient(SimpleClient):

    @classmethod
    def init(cls, mapper):
        cls.executor = Executor(mapper)
        return cls

    def listen(self, message):
        self.add_resp(self.executor(message))