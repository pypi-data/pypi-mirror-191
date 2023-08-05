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


class ModifyBandwidthPackageIpBandwidthRequest(JDCloudRequest):
    """
    
修改共享带宽包内弹性公网 IP 的带宽上限。

## 接口说明

- 共享带宽包中弹性公网IP的带宽上限不能高于共享带宽包的带宽上限。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ModifyBandwidthPackageIpBandwidthRequest, self).__init__(
            '/regions/{regionId}/bandwidthPackages/{bandwidthPackageId}:modifyBandwidthPackageIpBandwidth', 'POST', header, version)
        self.parameters = parameters


class ModifyBandwidthPackageIpBandwidthParameters(object):

    def __init__(self,regionId, bandwidthPackageId, bandwidthPackageIPSpecs):
        """
        :param regionId: Region ID
        :param bandwidthPackageId: 共享带宽包ID
        :param bandwidthPackageIPSpecs: Ip列表
        """

        self.regionId = regionId
        self.bandwidthPackageId = bandwidthPackageId
        self.bandwidthPackageIPSpecs = bandwidthPackageIPSpecs

