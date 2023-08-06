#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
import io
from datetime import datetime

from mesh.environ import Mode
from mesh.log.types import Logger, Level


class NopLogger(Logger):

    def __init__(self):
        self.__level__ = Level.INFO

    def name(self) -> str:
        return 'mesh'

    def info(self, fmt: str, *args: object):
        self.write(Level.INFO, fmt, *args)

    def warn(self, fmt: str, *args: object):
        self.write(Level.WARN, fmt, *args)

    def error(self, fmt: str, *args: object):
        self.write(Level.ERROR, fmt, *args)

    def debug(self, fmt: str, *args: object):
        self.write(Level.DEBUG, fmt, *args)

    def fatal(self, fmt: str, *args: object):
        self.write(Level.FATAL, fmt, *args)

    def stack(self, fmt: str, *args: object):
        self.write(Level.STACK, fmt, *args)

    def writer(self) -> io.BytesIO:
        return io.BytesIO()

    def level(self, level: Level):
        self.__level__ = level

    def write(self, level: Level, fmt: str, *args):
        if not level.match(self.__level__):
            return

        # discard log
        if not (Mode.Nolog.enable()):
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {level.name} {fmt}")
