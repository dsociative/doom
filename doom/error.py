# -*- coding: utf8 -*-


class UnexpectedException(Exception):
    def __str__(self):
        return 'unexpected error'


class CommandError(Exception):
    pass


class ParamNotFound(CommandError):
    def __str__(self):
        return '%s param not found' % self.args


class RequiredNotFound(CommandError):
    def __str__(self):
        return '%s required not found' % self.args