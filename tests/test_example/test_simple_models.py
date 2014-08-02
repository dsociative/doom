# -*- coding: utf8 -*-
from tests.base_test import BaseTest


class SimpleModelsTest(BaseTest):
    def test_login(self):
        self.send({'login': 'somelogin'})

        self.eq(
            self.recv(),
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