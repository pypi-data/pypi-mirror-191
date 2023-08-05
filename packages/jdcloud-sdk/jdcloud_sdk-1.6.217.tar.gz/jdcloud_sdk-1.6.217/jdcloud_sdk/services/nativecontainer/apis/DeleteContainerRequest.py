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


class DeleteContainerRequest(JDCloudRequest):
    """
    容器状态必须为 stopped、running 或 error状态。 <br>
按量付费的实例，如不主动删除将一直运行，不再使用的实例，可通过本接口主动停用。<br>
只能支持主动删除按配置计费类型的实例。包年包月过期的容器也可以删除，其它的情况还请发工单系统。计费状态异常的容器无法删除。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DeleteContainerRequest, self).__init__(
            '/regions/{regionId}/containers/{containerId}', 'DELETE', header, version)
        self.parameters = parameters


class DeleteContainerParameters(object):

    def __init__(self,regionId, containerId):
        """
        :param regionId: Region ID
        :param containerId: Container ID
        """

        self.regionId = regionId
        self.containerId = containerId

