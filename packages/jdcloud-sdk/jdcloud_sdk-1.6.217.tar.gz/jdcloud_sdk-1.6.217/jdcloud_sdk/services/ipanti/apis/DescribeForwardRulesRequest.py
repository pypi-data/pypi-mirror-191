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


class DescribeForwardRulesRequest(JDCloudRequest):
    """
    查询某个实例下的非网站转发配置
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(DescribeForwardRulesRequest, self).__init__(
            '/regions/{regionId}/instances/{instanceId}/forwardRules', 'GET', header, version)
        self.parameters = parameters


class DescribeForwardRulesParameters(object):

    def __init__(self, regionId,instanceId,):
        """
        :param regionId: 区域 ID, 高防不区分区域, 传 cn-north-1 即可
        :param instanceId: 高防实例 Id
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.pageNumber = None
        self.pageSize = None
        self.searchType = None
        self.searchValue = None
        self.sorts = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码, 默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小, 默认为10, 取值范围[10, 100]
        """
        self.pageSize = pageSize

    def setSearchType(self, searchType):
        """
        :param searchType: (Optional) 查询类型名称, domain:源站域名, ip:源站 IP, port: 转发端口, originPort: 源站端口, serviceIp: 高防IP(仅支持BGP线路的实例)
        """
        self.searchType = searchType

    def setSearchValue(self, searchValue):
        """
        :param searchValue: (Optional) 查询类型值
        """
        self.searchValue = searchValue

    def setSorts(self, sorts):
        """
        :param sorts: (Optional) 排序属性：
port - 按转发端口排序，默认不排序,asc表示按转发端口升序，desc表示按转发端口降序

        """
        self.sorts = sorts

