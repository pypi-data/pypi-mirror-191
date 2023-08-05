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


class ModifyInstanceVoucherAttributeRequest(JDCloudRequest):
    """
    修改实例抵扣券的 名称 和 描述。<br>
name 和 description 必须要指定一个

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyInstanceVoucherAttributeRequest, self).__init__(
            '/regions/{regionId}/instanceVouchers/{instanceVoucherId}:modifyInstanceVoucherAttribute', 'PATCH', header, version)
        self.parameters = parameters


class ModifyInstanceVoucherAttributeParameters(object):

    def __init__(self, regionId, instanceVoucherId, ):
        """
        :param regionId: 地域 ID
        :param instanceVoucherId: 实例抵扣券 ID
        """

        self.regionId = regionId
        self.instanceVoucherId = instanceVoucherId
        self.name = None
        self.description = None

    def setName(self, name):
        """
        :param name: (Optional) 实例抵扣券名称
        """
        self.name = name

    def setDescription(self, description):
        """
        :param description: (Optional) 实例抵扣券描述
        """
        self.description = description

