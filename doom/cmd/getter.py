# -*- coding: utf8 -*-

NOT_INIT = object()


class getter(object):
    def __init__(self, func):
        self.func = func
        self.requirements = func.func_code.co_varnames[1:]
        self.value = NOT_INIT

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class GetterStore(type):
    STORE = '_getters'

    def __new__(mcs, name, bases, dct):
        getters = {}
        for base in bases:
            getters.update(base.__dict__.get(mcs.STORE, {}))

        return super(GetterStore, mcs).__new__(
            mcs, name, bases, dict(mcs.process_dict(dct, getters))
        )

    @classmethod
    def process_dict(cls, dct, getters):
        for name, field in dct.items():
            if not isinstance(field, getter):
                yield name, field
            else:
                getters[name] = field

        yield cls.STORE, getters


class GetterHandler(object):
    __metaclass__ = GetterStore

    def __execute_getter(self, getter):
        return getter(*self._get_requirements(getter.requirements))

    def _do_get(self, name, getter):
        value = self.__execute_getter(getter)
        setattr(self, name, value)
        return value

    def _get_or_do(self, name):
        req = getattr(self, name, None)
        if req:
            return req
        else:
            return self._do_get(name, self._getters[name])

    def __init__(self, *args, **kwargs):
        super(GetterHandler, self).__init__(*args, **kwargs)
        for name in self._getters:
            self._get_or_do(name)

    def _get_requirements(self, requirements):
        yield self

        for name in requirements:
            yield self._get_or_do(name)
