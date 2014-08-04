# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod
from unittest import skipIf
from tests.base_test import BaseTest
from tests.utils import no_epoll

from socket_server.util.sender import Sender


@skipIf(no_epoll(), "can't import epoll on you os")
class BaseTalkerTest(BaseTest):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_talker_process(self):
        pass

    def setUp(self):
        super(BaseTalkerTest, self).setUp()
        self.talker_process = self.init_talker_process()
        self.talker_process.start()
        self.sender = Sender('', 8885)
        self.sender.connect()

    def tearDown(self):
        self.talker_process.terminate()

    def send(self, msg):
        self.sender.send(msg)

    def receive(self):
        sid, msg = self.sender.recv()
        return msg