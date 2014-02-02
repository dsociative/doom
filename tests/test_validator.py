# -*- coding: utf8 -*-
from doom.cmd.validator import CmdValidatorMixin
from doom.error import ParamNotFound, RequiredNotFound
from tests.base_test import BaseTest


class ParamCommand(CmdValidatorMixin):
    params = 'one', 'two'


class RequiredCommand(CmdValidatorMixin):
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

