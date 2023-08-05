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


class SetIpBlackListRequest(JDCloudRequest):
    """
    设置ip黑名白单
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(SetIpBlackListRequest, self).__init__(
            '/domain/{domain}/ipBlackList', 'POST', header, version)
        self.parameters = parameters


class SetIpBlackListParameters(object):

    def __init__(self,domain, ):
        """
        :param domain: 用户域名
        """

        self.domain = domain
        self.ips = None
        self.ipListType = None

    def setIps(self, ips):
        """
        :param ips: (Optional) ip名单,ips中url不能超过50条，中国境外/全球加速域名暂不支持传IP段
        """
        self.ips = ips

    def setIpListType(self, ipListType):
        """
        :param ipListType: (Optional) ip黑白名单类型，black:黑名单,white:白名单
        """
        self.ipListType = ipListType

