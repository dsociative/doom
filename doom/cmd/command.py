# -*- coding: utf8 -*-
from doom.cmd.validator import CmdValidatorMixin


class Command(CmdValidatorMixin):
    def __init__(self, params):
        self.p = params

    def log_items(self):
        """
        Template function for extend Executor log data
        """
        return tuple()