# -*- coding: utf8 -*-
from doom.executor import Executor
from doom.general import General
import os
import pytest
from redis import Redis
from rmodel.fields.rfield import rfield
from rmodel.models.rstore import RStore


@pytest.fixture(scope='function')
def general(request):
    redis = Redis()

    class TestGeneral(General):
        def init_root(self):
            return RootModel(redis=redis)

        def init_executor(self):
            return Executor({})

    request.addfinalizer(redis.flushall)
    return TestGeneral()


class RootModel(RStore):
    root = True

    field = rfield()


def test_redis(general):
    assert isinstance(general.root, RootModel)
    assert isinstance(general.root.field, rfield)
    general.root.field.set('value')
    assert general.root.field.get() == 'value'


def test_check_value(general):
    assert general.root.field.get() is None


def test_path(general):
    assert general.path() == os.path.dirname(__file__)