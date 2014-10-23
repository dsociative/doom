# -*- coding: utf8 -*-
from doom.social.signature.base_signature import BaseSignature


class ODSignature(BaseSignature):
    def key_value(self, args):
        return args

    def auth(self, params, sig):
        return self.check(
            [
                params.get('logged_user_id', ''),
                params.get('session_key', '')
            ],
            sig
        )