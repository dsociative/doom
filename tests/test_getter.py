# -*- coding: utf8 -*-
from doom.cmd.getter import GetterStore, getter, GetterHandler
import pytest


class MockClass(object):
    __metaclass__ = GetterStore

    def __init__(self, nick):
        self.nick = nick
        super(MockClass, self).__init__()

    @getter
    def user(self):
        return {'some': self.nick}


def test_getter_decorator():
    m = MockClass('doom')
    assert not hasattr(m, 'user')
    assert isinstance(m._getters['user'], getter)
    assert m._getters['user'](m) == {'some': 'doom'}


def test_getter_decorator_parse_requirements():
    g = getter(lambda self, user, player: 1)
    assert g.requirements == ['user', 'player']


def test_getter_requirements():
    h = GetterHandler()
    assert list(h._get_requirements([])) == [h]
    h._getters['player'] = getter(lambda self: {'player': '1'})
    assert list(h._get_requirements(('player',))) == [h, {'player': '1'}]


class MockCommand(MockClass, GetterHandler):
    def __init__(self, params):
        self.p = params
        super(MockCommand, self).__init__(params)

    def __call__(self, *args, **kwargs):
        self._get_all()
        return self

    @getter
    def uid(self):
        return self.p['uid']

    @getter
    def some_none(self):
        return None

    @getter
    def digit(self):
        return 1


def test_getter_error():
    command = MockCommand({})
    with pytest.raises(KeyError):
        command._get_all()


def test_getter_handler():
    command = MockCommand({'uid': 'doom'})()
    assert isinstance(command._getters['user'], getter)
    assert command.uid == 'doom'
    assert command.some_none is None
    assert command.digit == 1


class HandlerWithRequirements(MockClass, GetterHandler):
    @getter
    def friend(self, user):
        return {'i friend': user}


def test_handler_with_requirements():
    m = HandlerWithRequirements('somename')
    m._get_all()
    assert m.friend == {'i friend': {'some': 'somename'}}


v = 0


def test_handler_cached_getter_execute():
    class TestHandler(GetterHandler):
        @getter
        def zdigit(self):
            global v
            v += 1
            return v

        @getter
        def value1(self, zdigit):
            return "value1: %s" % zdigit

        @getter
        def value2(self, zdigit):
            return "value2: %s" % zdigit

    h = TestHandler()
    h._get_all()
    assert h.zdigit == 1
    assert h.value1 == "value1: 1"
    assert h.value2 == "value2: 1"