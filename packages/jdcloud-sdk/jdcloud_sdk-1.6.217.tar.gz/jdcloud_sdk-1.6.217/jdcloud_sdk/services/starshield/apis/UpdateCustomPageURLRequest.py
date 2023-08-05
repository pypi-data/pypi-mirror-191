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


class UpdateCustomPageURLRequest(JDCloudRequest):
    """
    更新自定义页面URL
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(UpdateCustomPageURLRequest, self).__init__(
            '/zones/{zone_identifier}/custom_pages/{identifier}', 'PUT', header, version)
        self.parameters = parameters


class UpdateCustomPageURLParameters(object):

    def __init__(self,zone_identifier, identifier, ):
        """
        :param zone_identifier: 
        :param identifier: 
        """

        self.zone_identifier = zone_identifier
        self.identifier = identifier
        self.url = None
        self.state = None

    def setUrl(self, url):
        """
        :param url: (Optional) 与自定义页面关联的URL。
        """
        self.url = url

    def setState(self, state):
        """
        :param state: (Optional) 自定义页面状态
        """
        self.state = state

