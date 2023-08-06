#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from typing import Any

from mesh.macro import spi
from mesh.mpc import Provider


@spi("http")
class HTTPProvider(Provider):

    def start(self, address: str, tc: Any):
        pass

    def close(self):
        pass
