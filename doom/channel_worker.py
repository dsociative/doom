# -*- coding: utf8 -*-
import atexit
import zmq
import signal


class ChannelWorker(object):
    def __init__(self, channel):
        self.channel = channel
        self.running = False

    def init_socket(self):
        self.context = zmq.Context(1)
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(self.channel)

    def process(self, message):
        Exception('Template method')

    def run(self):
        self.init_socket()
        self.on_exit()
        self.prepare()

        self.running = True
        while self.running:
            self.process(self.socket.recv_json())

    def exit(self, *args):
        self.running = False

    def on_exit(self):
        signal.signal(signal.SIGTERM, self.exit)

    def prepare(self):
        """
        Template Method
        """
