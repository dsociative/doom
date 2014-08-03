# -*- coding: utf8 -*-
from doom.cmd.command import Command


class UserAuth(Command):
    name = 'user.auth'

    def __call__(self, *args, **kwargs):
        return {'whut': 'u doin?'}