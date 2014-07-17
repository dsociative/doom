# -*- coding: utf8 -*-
from multiprocessing import Process, Value
import subprocess
import time
import signal

from doom.channel_worker import ChannelWorker
import os
from tests.base_test import BaseTest
import zmq


class TestWorker(ChannelWorker, Process):
    def __init__(self, channel, flag):
        ChannelWorker.__init__(self, channel)
        Process.__init__(self)
        self.flag = flag

    def process(self, message):
        assert subprocess.call(['sleep', '2']) == 0
        self.flag.value += 1

    def kill(self):
        os.kill(self.pid, signal.SIGKILL)


class ChannelWorkerTest(BaseTest):
    def setUp(self):
        self.flag = Value('d', 0)
        self.channel = 'ipc:///tmp/channel_doom_test'
        self.worker = TestWorker(self.channel, self.flag)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect(self.channel)
        self.worker.start()

    def tearDown(self):
        self.worker.terminate()

    def test_send(self):
        self.socket.send_json({'msg': 1}, flags=zmq.NOBLOCK)

    def test_gracefull_shutdown(self):
        self.socket.send_json({'do': 1}, flags=zmq.NOBLOCK)
        time.sleep(0.3)
        self.worker.terminate()
        time.sleep(2)
        self.eq(self.flag.value, 1)

    def test_kill(self):
        self.socket.send_json({'do': 1}, flags=zmq.NOBLOCK)
        self.worker.kill()
        self.eq(self.flag.value, 0)
