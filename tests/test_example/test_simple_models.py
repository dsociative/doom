# -*- coding: utf8 -*-

from doom.example.simple_models import SimpleModelsProcess
from tests.base_talker_test import BaseTalkerTest


class SimpleModelsTest(BaseTalkerTest):
    def init_talker_process(self):
        return SimpleModelsProcess()

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