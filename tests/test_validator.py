# -*- coding: utf8 -*-
from command.command_mixin import CommandMixin
from command.error import ParamNotFound, RequiredNotFound
from tests.base_test import BaseTest


class ParamCommand(CommandMixin):
    params = 'one', 'two'


class RequiredCommand(CommandMixin):
    requires = 'model1', 'model2'


class TestParamValidator(BaseTest):
    def setUp(self):
        super(TestParamValidator, self).setUp()
        self.command = ParamCommand()

    def test_param_not_found(self):
        self.raises_re(
            ParamNotFound, 'two param not found',
            self.command.validate_params, {'one': 1}
        )
        self.raises_re(
            ParamNotFound, 'one param not found',
            self.command.validate_params, {'two': 2}
        )

    def test_all_params(self):
        self.eq(self.command.validate_params({'one': 1, 'two': 2}), None)


class TestRequiredValidator(BaseTest):
    def setUp(self):
        super(TestRequiredValidator, self).setUp()
        self.command = RequiredCommand()

    def test_required_not_found(self):
        obj = object()
        self.raises_re(
            RequiredNotFound, 'model1 required not found',
            self.command.validate_required, obj
        )
        obj = type('obj', (object,), {'model1': 0})
        self.raises_re(
            RequiredNotFound, 'model2 required not found',
            self.command.validate_required, obj
        )

    def test_all_requred(self):
        obj = type('obj', (object,), {'model1': 0, 'model2': False})
        self.eq(self.command.validate_required(obj), None)