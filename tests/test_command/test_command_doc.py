# -*- coding: utf8 -*-
from collections import defaultdict
from class_collector import ClassCollector
from doom.cmd.doc import CommandDoc

from tests.base_test import BaseTest
from tests.test_command.test_command_env.test_command import TestCommand


class TestCommandDoc(BaseTest):
    def setUp(self):
        self.mapper = ClassCollector(
            'tests/test_command/test_command_env',
            TestCommand
        ).mapper()
        self.command_doc = CommandDoc(
            'Command',
            'tests/tmp',
            self.mapper,
        )

    def test_mapper(self):
        self.eq(
            str(self.mapper['battle.kill']),
            "<class 'battle_kill.BattleKill'>"
        )
        self.eq(
            str(self.mapper['user.auth']),
            "<class 'user_auth.UserAuth'>"
        )
        self.eq(len(self.mapper), 2)

    def test_build_tree(self):
        expected = defaultdict(
            defaultdict,
            {
                'battle': {'kill': '.battle_kill.BattleKill'},
                'user': {'auth': '.user_auth.UserAuth'},
            }
        )
        self.eq(self.command_doc.build_tree(self.mapper), expected)

    def test_render(self):
        self.eq(
            self.command_doc.render_item(
                'battle',
                {
                    'kill': '.battle_kill.BattleKill',
                    'live': '.battle_kill.BattleLive',
                }
            ),
            '''battle
==========


battle.live
---------------

.. autoclass:: .battle_kill.BattleLive
    :members:

battle.kill
---------------

.. autoclass:: .battle_kill.BattleKill
    :members:
'''
        )

    def test_render_index(self):
        self.eq(
            self.command_doc.render_index(
                'Command', ('battle', 'user')
            ),
            '''Command
===========


.. toctree::


    battle

    user
'''
        )

    def test_make_files(self):
        self.command_doc.make_files()
        for n in self.command_doc.tree:
            self.eq(
                open('tests/tmp/%s.rst' % n).read(),
                self.command_doc.render_item(n, self.command_doc.tree[n])
            )

        self.eq(
            open('tests/tmp/index.rst').read(),
            self.command_doc.render_index(
                'Command', self.command_doc.tree.keys()
            ),
        )
