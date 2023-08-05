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


class DescribeSchemaSpaceTopRequest(JDCloudRequest):
    """
    库空间Top 10
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(DescribeSchemaSpaceTopRequest, self).__init__(
            '/regions/{regionId}/instance/{instanceGid}/schemaSpaceTop', 'GET', header, version)
        self.parameters = parameters


class DescribeSchemaSpaceTopParameters(object):

    def __init__(self, regionId,instanceGid,):
        """
        :param regionId: 地域代码，取值范围参见[《各地域及可用区对照表》](../Enum-Definitions/Regions-AZ.md)
        :param instanceGid: RDS 实例ID，唯一标识一个RDS实例。
        """

        self.regionId = regionId
        self.instanceGid = instanceGid
        self.sortField = None
        self.sortType = None

    def setSortField(self, sortField):
        """
        :param sortField: (Optional) 排序字段：表空间(totalSize)、表数据空间(dataSize)、索引空间(idxSize)、碎片率(fragment)、行数(dataRows)
        """
        self.sortField = sortField

    def setSortType(self, sortType):
        """
        :param sortType: (Optional) 排序类型，desc 降序、asc 升序，默认降序
        """
        self.sortType = sortType

