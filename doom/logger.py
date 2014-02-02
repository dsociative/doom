# -*- coding: utf8 -*-
from datetime import datetime
import json
from traceback import print_exc


def now():
    return datetime.now().isoformat()


class Logger(object):
    def __init__(self, out, err):
        self.out = out
        self.err = err

    def dump(self, msg):
        return json.dumps(msg, separators=(',', ': '), ensure_ascii=False)

    def items(self, route, command, msg):
        return (now(), route) + command.log_items() + (self.dump(msg),)

    def log(self, route, command, msg):
        self.out.write(
            '\t'.join(map(str, self.items(route, command, msg))) + '\n'
        )

    def request(self, command, msg):
        self.log('in', command, msg)

    def responses(self, command, responses):
        for response in responses:
            self.log('out', command, response)
        self.out.flush()
        return responses

    def unexpected_exception(self, command):
        """
        Template method for logging unexpected errors
        """
        print_exc(file=self.err)
