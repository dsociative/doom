# -*- coding: utf8 -*-
from doom.social.signature.base_signature import BaseSignature


class VKSignature(BaseSignature):
    PREFIX = '_'

    def __init__(self, secretkey):
        super(VKSignature, self).__init__(secretkey, self.PREFIX)

    def key_value(self, args):
        return self.prefix.join(map(str, args))

    def string(self, args):
        return self.prefix.join((self.key_value(args), self.key))

    def auth(self, param):
        return self.check(
            (
                param.get('api_id', ''), param.get('viewer_id', '')
            ),
            param.get('auth_key', '')
        )