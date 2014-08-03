# -*- coding: utf8 -*-
from multiprocessing import Process
from class_collector import ClassCollector

from doom.cmd.command import Command


class SimpleModelsProcess(Process):
    def __init__(self):
        super(SimpleModelsProcess, self).__init__()
        from socket_server.base.talker import Talker
        from doom.executor_client import ExecutorClient

        self.talker = Talker(
            client_cls=ExecutorClient.init(
                ClassCollector('doom/example/simple_commands', Command).mapper()
            )
        )

    def run(self):
        self.talker.run()