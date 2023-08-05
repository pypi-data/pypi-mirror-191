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


class UpdateDNSRecordRequest(JDCloudRequest):
    """
    
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateDNSRecordRequest, self).__init__(
            '/zones/{zone_identifier}/dns_records/{identifier}', 'PUT', header, version)
        self.parameters = parameters


class UpdateDNSRecordParameters(object):

    def __init__(self,zone_identifier, identifier, name, content, ttl, ):
        """
        :param zone_identifier: 
        :param identifier: 
        :param name: DNS记录名称
        :param content: DNS记录内容
        :param ttl: DNS记录的生存时间。值为1是 "自动"。
        """

        self.zone_identifier = zone_identifier
        self.identifier = identifier
        self.ty_pe = None
        self.name = name
        self.content = content
        self.ttl = ttl
        self.proxied = None
        self.priority = None
        self.srvData = None
        self.caaData = None

    def setTy_pe(self, ty_pe):
        """
        :param ty_pe: (Optional) DNS记录类型
        """
        self.ty_pe = ty_pe

    def setProxied(self, proxied):
        """
        :param proxied: (Optional) 是否利用星盾的性能和安全优势
        """
        self.proxied = proxied

    def setPriority(self, priority):
        """
        :param priority: (Optional) 如果是MX记录，该属性是必需的
        """
        self.priority = priority

    def setSrvData(self, srvData):
        """
        :param srvData: (Optional) 
        """
        self.srvData = srvData

    def setCaaData(self, caaData):
        """
        :param caaData: (Optional) 
        """
        self.caaData = caaData

