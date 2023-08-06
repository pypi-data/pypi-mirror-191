#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
import signal
import threading

import mesh.asm as asm
from mesh.boost import *
from mesh.cause import *
from mesh.codec import *
from mesh.context import *
from mesh.macro import *
from mesh.mpc import *
from mesh.prsim import *

__all__ = (
    "mpi",
    "mps",
    "index",
    "spi",
    "binding",
    "Codeable",
    "Cause",
    "Inspector",
    "Types",
    "ServiceLoader",
    ##
    "URN",
    "URNFlag",
    "Consumer",
    "Filter",
    "Invocation",
    "Provider",
    "Schema",
    "ServiceProxy",
    "MeshKey",
    "Mesh",
    ##
    "MeshException",
    "CompatibleException",
    "NotFoundException",
    "ValidationException",
    "Codec",
    ##
    "Cache",
    "Cluster",
    "Configurator",
    "Context",
    "Cryptor",
    "DataHouse",
    "Dispatcher",
    "Licenser",
    "Locker",
    "Network",
    "Publisher",
    "Registry",
    "Routable",
    "RuntimeHook",
    "Scheduler",
    "Sequence",
    "Subscriber",
    "Tokenizer",
    "Key",
    "IOStream",
    "Hodor",
    "Transport",
    "Session",
    "KV",
    "Evaluator",
    #
    "Runtime"
)

__mesh_runtime__ = Mooter()


def init():
    asm.init()


def start():
    __mesh_runtime__.start()


def refresh():
    __mesh_runtime__.refresh()


def stop():
    __mesh_runtime__.stop()


def wait():
    """
    Use signal handler to throw exception which can be caught to allow graceful exit.
    :return:
    """
    waiter = threading.Event()

    def signal_handler(signum, frame):
        try:
            stop()
        finally:
            waiter.set()

    signal.signal(signal.SIGTERM, signal_handler)
    waiter.wait()
