# -*- coding: utf8 -*-
from socket_server.util.sender import Sender

from doom.example.hello_talker import HelloTalkerProcess
from tests.base_test import BaseTest
from unittest2 import skipIf


def no_epoll(*args):
    try:
        from select import EPOLLIN
        return False
    except ImportError:
        return True


@skipIf(no_epoll(), "can't import epoll on you os")
class TalkerTest(BaseTest):
    def setUp(self):
        super(TalkerTest, self).setUp()
        self.talker_process = HelloTalkerProcess()
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

    def test_send_receive(self):
        self.send({'command': 'hello.talker'})
        self.eq(self.receive(), '{"hello": "world"}')
