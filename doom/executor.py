# -*- coding: utf8 -*-
import sys
from doom.error import CommandError, UnexpectedException
from doom.logger import Logger


class Executor(object):
    unexpected_exception = UnexpectedException()

    def __init__(self, mapper, stdout=sys.stdout, stderr=sys.stderr,
                 logger_cls=Logger):
        self.mapper = mapper
        self.logger = logger_cls(stdout, stderr)

    def get_command(self, msg):
        return self.mapper.get(msg.get('command'))

    def error(self, command, exception):
        """
        Template method for customization errors
        """
        return str(exception)

    def try_execute(self, command):
        try:
            return command()
        except CommandError as exception:
            return self.error(command, exception)
        except:
            self.logger.unexpected_exception(command)
            return self.error(command, self.unexpected_exception)

    def exec_command(self, command_cls, msg):
        command = command_cls(msg)
        self.logger.request(command, msg)
        responses = self.try_execute(command)

        self.logger.responses(command, responses)
        return responses

    def __call__(self, msg):
        return self.exec_command(self.get_command(msg), msg)
