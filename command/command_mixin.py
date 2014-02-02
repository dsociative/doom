# -*- coding: utf8 -*-
from command.error import ParamNotFound, RequiredNotFound


class CommandMixin(object):
    params = tuple()
    requires = tuple()

    def validate_params(self, params):
        for name in self.params:
            if name not in params:
                raise ParamNotFound(name)

    def validate_required(self, store):
        for name in self.requires:
            if getattr(store, name, None) is None:
                raise RequiredNotFound(name)