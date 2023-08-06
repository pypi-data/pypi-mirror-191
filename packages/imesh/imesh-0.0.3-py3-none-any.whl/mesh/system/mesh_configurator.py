#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from mesh.kinds import Profile
from mesh.macro import spi
from mesh.prsim import Configurator


@spi("mesh")
class MeshConfigurator(Configurator):

    def push(self, profile: Profile) -> None:
        """"""
        pass

    def pull(self, data_id: str) -> Profile:
        """"""
        pass
