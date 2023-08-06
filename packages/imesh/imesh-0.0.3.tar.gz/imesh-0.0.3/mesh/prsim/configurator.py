#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

from abc import ABC, abstractmethod

from mesh.kinds.profile import Profile
from mesh.macro import mpi
from mesh.macro import spi


class Watcher(ABC):

    @abstractmethod
    def receive(self, profile: Profile) -> None:
        """
        Trigger when change event subscribe from mesh node.
        :param profile: data profile
        :return:
        """
        pass


@spi("mesh")
class Configurator(ABC):

    @abstractmethod
    @mpi("mesh.profile.publish")
    def push(self, profile: Profile) -> None:
        """
        Push the profile to bind data id.
        :param profile: data profile
        :return:
        """
        pass

    @abstractmethod
    @mpi("mesh.profile.pull")
    def pull(self, data_id: str) -> Profile:
        """
        Load the profiles by data id.
        :param data_id: data id
        :return: data profiles
        """
        pass

    def watch(self, data_id: str, watcher: Watcher) -> None:
        """
        Watch the profile.
        :param data_id: data id
        :param watcher: data watcher
        :return:
        """
        pass
