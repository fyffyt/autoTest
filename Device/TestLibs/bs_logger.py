#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import logging
import time
import inspect

class BSLogger(object):
    def __init__(self, filename):
        abspath = os.path.join(
                os.path.abspath(os.path.dirname(inspect.stack()[1][1])),
                filename
                )

        self._logger = logging.getLogger()
        self._logger.addHandler(logging.FileHandler(abspath))

        # just search log level conf in nearest caller and farmost caller
        frame_depth1 = sys._getframe(1)
        if frame_depth1.f_globals.has_key("LOGGING_LEVEL"):
            self._logger.setLevel(frame_depth1.f_globals['LOGGING_LEVEL'])
        else:
            frame_depth2 = inspect.stack()[-1][0]
            if frame_depth2.f_globals.has_key("LOGGING_LEVEL"):
                self._logger.setLevel(frame_depth2.f_globals['LOGGING_LEVEL'])
            else:
                raise NotImplementedError("Initiate logger failed, please specify "
                        + "logging level by define a global variable\n"
                        + "\t\tLOGGING_LEVEL = logging.DEBUG|INFO|WARN|CRITICAL|FATAL\n")

    def i(self, msg):
        c = sys._getframe(1)
        self._logger.info("="*100 + '\n'
                + '[INFO] At %s, in %s, on line %s:\n'\
                        % (time.strftime("%Y-%m-%d-%H-%M-%S"),
                            c.f_code.co_filename,
                            c.f_lineno)
                + msg + '\n' + "+"*100)

    def d(self, msg):
        c = sys._getframe(1)
        self._logger.debug("="*100 + '\n'
                + '[DEBUG] At %s, in %s, on line %s:\n'\
                        % (time.strftime("%Y-%m-%d-%H-%M-%S"),
                            c.f_code.co_filename,
                            c.f_lineno)
                + msg + '\n' + "+"*100)

    def w(self, msg):
        c = sys._getframe(1)
        self._logger.warn("="*100 + '\n'
                + '[WARN] At %s, in %s, on line %s:\n'\
                        % (time.strftime("%Y-%m-%d-%H-%M-%S"),
                            c.f_code.co_filename,
                            c.f_lineno)
                + msg + '\n' + "+"*100)

    def e(self, msg):
        c = sys._getframe(1)
        self._logger.error("="*100 + '\n'
                + '[ERROR] At %s, in %s, on line %s:\n'\
                        % (time.strftime("%Y-%m-%d-%H-%M-%S"),
                            c.f_code.co_filename,
                            c.f_lineno)
                + msg + '\n' + "+"*100)

    def c(self, msg):
        c = sys._getframe(1)
        self._logger.critical("="*100 + '\n'
                + '[CRITICAL] At %s, in %s, on line %s:\n'\
                        % (time.strftime("%Y-%m-%d-%H-%M-%S"),
                            c.f_code.co_filename,
                            c.f_lineno)
                + msg + '\n' + "+"*100)

    def f(self, msg):
        c = sys._getframe(1)
        self._logger.fatal("="*100 + '\n'
                + '[FATAL] At %s, in %s, on line %s:\n'\
                        % (time.strftime("%Y-%m-%d-%H-%M-%S"),
                            c.f_code.co_filename,
                            c.f_lineno)
                + msg + '\n' + "+"*100)

