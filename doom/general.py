# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod
import os


class General(object):
    __metaclass__ = ABCMeta

    def __new__(cls):
        if not hasattr(cls, 'instance'):
             cls.instance = super(General, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.root = self.init_root()
        self.executor = self.init_executor()

    @abstractmethod
    def init_root(self):
        pass

    @abstractmethod
    def init_executor(self):
        pass

    def path(self):
        return os.path.dirname(__file__)
