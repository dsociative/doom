# -*- coding: utf8 -*-
from unittest import skipIf

from socket_server.util.sender import Sender

from doom.example.simple_models import SimpleModelsProcess
from tests.base_test import BaseTest
from tests.utils import no_epoll


@skipIf(no_epoll(), "can't import epoll on you os")
class SimpleModelsTest(BaseTest):
    def setUp(self):
        super(SimpleModelsTest, self).setUp()
        self.talker_process = SimpleModelsProcess()
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

    def test_login(self):
        self.send({'login': 'somelogin', 'command': 'user.auth'})

        self.eq(
            self.receive(),
            {
                'simple': {
                    'users': {
                        'somelogin': {
                            'power': 1
                        }
                    }
                }
            }
        )