#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

from enum import Enum


class MeshFlag(Enum):
    HTTP = "00", "http"
    GRPC = "01", "grpc"
    MQTT = "02", "mqtt"
    TCP = "03", "tcp"

    JSON = "00", "json"
    PROTOBUF = "01", "protobuf"
    XML = "02", "xml"
    THRIFT = "03", "thrift"
    YAML = "04", "yaml"

    def get_code(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

    @staticmethod
    def of_proto(code: str) -> "MeshFlag":
        for member in MeshFlag:
            if member.value and member.value[0] == code:
                return member
        return MeshFlag.HTTP

    @staticmethod
    def of_code(code: str) -> "MeshFlag":
        for member in MeshFlag:
            if member.value and member.value[0] == code:
                return member
        return MeshFlag.JSON

    @staticmethod
    def of_name(name: str) -> "MeshFlag":
        for member in MeshFlag:
            if member.value and member.value[1] == name:
                return member
        return MeshFlag.HTTP
