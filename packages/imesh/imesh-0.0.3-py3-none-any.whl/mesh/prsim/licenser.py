#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#
from abc import ABC, abstractmethod
from typing import Dict

from mesh.kinds import License
from mesh.macro import mpi


class Licenser(ABC):

    @abstractmethod
    @mpi(name="mesh.license.imports", encrypt=True)
    def imports(self, text: str):
        """
        Import the license.
        :param text:
        :return:
        """
        pass

    @abstractmethod
    @mpi(name="mesh.license.exports", encrypt=True)
    def exports(self) -> str:
        """
        Exports the license.
        :return:
        """
        pass

    @abstractmethod
    @mpi(name="mesh.license.explain", encrypt=True)
    def explain(self) -> License:
        """
        Explain the license.
        :return:
        """
        pass

    @abstractmethod
    @mpi(name="mesh.license.verify", encrypt=True)
    def verify(self) -> bool:
        """
        Verify the license.
        :return:
        """
        pass

    @abstractmethod
    @mpi(name="mesh.license.features", encrypt=True)
    def features(self) -> Dict[str, str]:
        """
        License features.
        :return:
        """
        pass
