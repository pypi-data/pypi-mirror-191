# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class CreateSecretRequest(JDCloudRequest):
    """
    创建一个 secret，用于存放镜像仓库机密相关信息。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateSecretRequest, self).__init__(
            '/regions/{regionId}/secrets', 'POST', header, version)
        self.parameters = parameters


class CreateSecretParameters(object):

    def __init__(self,regionId, name, secretType, data):
        """
        :param regionId: Region ID
        :param name: 机密数据名称，不能重复

        :param secretType: 机密数据的类型，目前仅支持：docker-registry 类型，用来和docker registry认证的类型。

        :param data: 机密的数据。<br>
key 的有效字符包括字母、数字、-、_和.； <br>
value 是 Base64 编码的字符串，不能包含换行符（在 linux 下使用 base64 -w 0选项），每个value长度上限为4KB，整个data的长度不能超过256KB; <br>
必须包含server、username、password 字段，email 字段是可选的。<br>

        """

        self.regionId = regionId
        self.name = name
        self.secretType = secretType
        self.data = data

