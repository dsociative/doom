# -*- coding: utf8 -*-
from StringIO import StringIO
from doom.cmd.command import Command
from doom.executor import Executor
from tests.base_test import BaseTest


class DescribeMarsellusWallace(Command):
    def __call__(self, *a):
        return 'What...?'


class ManyParams(Command):
    params = 'param', 'param2'

    def __call__(self):
        self.validate_params(self.p)


class UnexpectedError(Command):
    def __call__(self, this_is_error):
        pass


class TwoResponse(Command):
    def __call__(self):
        return ['one', 'two']


class ExtendedLogging(Command):
    def log_items(self):
        return self.p, 'something', 0


class TestExecutor(BaseTest):
    def setUp(self):
        super(TestExecutor, self).setUp()
        self.stderr = StringIO()
        self.stdout = StringIO()
        self.executor = Executor(
            {
                'Describe.MarsellusWallace': DescribeMarsellusWallace,
                'many.params': ManyParams,
                'unexpected.error': UnexpectedError,
                'two.response': TwoResponse,
                'extened_logging': ExtendedLogging
            },
            stdout=self.stdout,
            stderr=self.stderr
        )

    def test_execute(self):
        self.eq(
            self.executor({'command': 'Describe.MarsellusWallace'}),
            'What...?'
        )

    def test_error_param(self):
        self.eq(
            self.executor({'command': 'many.params', 'param': 1}),
            'param2 param not found'
        )

    def test_unexpected_error(self):
        self.eq(
            self.executor({'command': 'unexpected.error'}),
            'unexpected error'
        )
        self.isin('Traceback', self.stderr.getvalue())

    def test_logging(self):
        self.executor({'command': 'two.response'})
        log = self.stdout.getvalue().split('\n')

        dt, route, msg = log[0].split('\t')
        self.eq(route, 'in')
        self.eq(msg, '{"command": "two.response"}')

        dt, route, msg = log[1].split('\t')
        self.eq(route, 'out')
        self.eq(msg, '"one"')

        dt, route, msg = log[2].split('\t')
        self.eq(route, 'out')
        self.eq(msg, '"two"')

    def test_logging_extended(self):
        self.executor({'command': 'extened_logging', 'param': 1, 'w': 'e'})
        log = self.stdout.getvalue().split('\n')

        dt, route, params, something, null, msg = log[0].split('\t')
        self.eq(route, 'in')
        self.eq(something, 'something')
        self.eq(null, '0')
        self.eq(msg, '{"command": "extened_logging","w": "e","param": 1}')
        self.eq(params, "{'command': 'extened_logging', 'w': 'e', 'param': 1}")
