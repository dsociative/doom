# -*- coding: utf8 -*-

from doom.example.hello_talker import HelloTalkerProcess
from tests.base_talker_test import BaseTalkerTest


class TestTalker(BaseTalkerTest):

    def init_talker_process(self):
        return HelloTalkerProcess()

    def test_send_receive(self):
        self.send({'command': 'hello.talker'})
        self.eq(self.receive(), '{"hello": "world"}')
