# -*- coding: utf-8 -*-
import hashlib
from doom.error import CommandError


class SignatureError(CommandError):
    def __str__(self):
        return 'signature error'


class BaseSignature(object):

    def __init__(self, key, prefix='='):
        self.prefix = prefix
        self.key = key

    def key_value(self, args):
        for kv in sorted(args.iteritems()):
            yield self.prefix.join(map(str, kv))

    def string(self, args):
        return ''.join(self.key_value(args)) + self.key

    def md5(self, args):
        return hashlib.md5(self.string(args)).hexdigest()

    def check(self, params, sig):
        print self.md5(params)
        print sig
        return self.md5(params) == sig

    def try_check(self, params):
        if not self.auth(params):
            raise SignatureError