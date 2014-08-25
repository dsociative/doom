# -*- coding: utf8 -*-
from doom.cmd.getter import GetterStore, getter, GetterHandler


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
    assert g.requirements == ('user', 'player')


class MockCommand(MockClass, GetterHandler):
    @getter
    def some_none(self):
        return None

    @getter
    def digit(self):
        return 1


def test_getter_requirements():
    h = GetterHandler()
    assert list(h._get_requirements([])) == [h]
    h._getters['player'] = getter(lambda self: {'player': '1'})
    assert list(h._get_requirements(('player',))) == [h, {'player': '1'}]


def test_getter_handler():
    command = MockCommand('doom')
    assert isinstance(command._getters['user'], getter)
    assert command.user == {'some': 'doom'}
    assert command.some_none is None
    assert command.digit == 1


class HandlerWithRequirements(MockClass, GetterHandler):
    @getter
    def friend(self, user):
        return {'i friend': user}


def test_handler_with_requirements():
    m = HandlerWithRequirements('somename')
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
    assert h.zdigit == 1
    assert h.value1 == "value1: 1"
    assert h.value2 == "value2: 1"