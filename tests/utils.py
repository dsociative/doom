# -*- coding: utf8 -*-
def no_epoll(*args):
    try:
        from select import EPOLLIN
        return False
    except ImportError:
        return True