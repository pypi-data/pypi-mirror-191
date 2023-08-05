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


class GetChallengeTTLSettingRequest(JDCloudRequest):
    """
    指定访问者在成功完成一项挑战（如验证码）后允许访问您的网站多长时间。在TTL过期后，访问者将不得不完成新的挑战。我们建议设置为15-45分钟，并将尝试遵守任何超过45分钟的设置。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(GetChallengeTTLSettingRequest, self).__init__(
            '/zones/{zone_identifier}/settings$$challenge_ttl', 'GET', header, version)
        self.parameters = parameters


class GetChallengeTTLSettingParameters(object):

    def __init__(self,zone_identifier):
        """
        :param zone_identifier: 
        """

        self.zone_identifier = zone_identifier

