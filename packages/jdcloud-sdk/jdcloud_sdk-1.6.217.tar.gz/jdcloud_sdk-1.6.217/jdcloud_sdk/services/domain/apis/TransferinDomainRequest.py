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


class TransferinDomainRequest(JDCloudRequest):
    """
    用于提交域名转入操作
要转入域名前，请确保用户的京东云账户有足够的资金支付，Openapi接口回返回订单号，可以用此订单号向计费系统查阅详情

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(TransferinDomainRequest, self).__init__(
            '/regions/{regionId}/transferin', 'POST', header, version)
        self.parameters = parameters


class TransferinDomainParameters(object):

    def __init__(self, regionId, domainName, passWord, templateId):
        """
        :param regionId: 实例所属的地域ID
        :param domainName: 域名
        :param passWord: 域名转移密码
        :param templateId: 模板ID
        """

        self.regionId = regionId
        self.domainName = domainName
        self.passWord = passWord
        self.templateId = templateId

