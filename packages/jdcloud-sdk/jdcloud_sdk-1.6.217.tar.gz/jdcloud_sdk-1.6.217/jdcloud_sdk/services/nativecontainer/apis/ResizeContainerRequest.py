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


class ResizeContainerRequest(JDCloudRequest):
    """
    调整原生容器实例类型配置。
- 原生容器状态为停止;
- 支持升配、降配；**不支持原有规格**
- 计费类型不变
    - 包年包月：需要计算配置差价，如果所选配置价格高，需要补齐到期前的差价，到期时间不变；如果所选配置价格低，需要延长到期时间
    - 按配置：按照所选规格，进行计费

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ResizeContainerRequest, self).__init__(
            '/regions/{regionId}/containers/{containerId}:resize', 'POST', header, version)
        self.parameters = parameters


class ResizeContainerParameters(object):

    def __init__(self,regionId, containerId, instanceType):
        """
        :param regionId: Region ID
        :param containerId: Container ID
        :param instanceType: 新实例类型，不可与原实例类型相同
        """

        self.regionId = regionId
        self.containerId = containerId
        self.instanceType = instanceType

