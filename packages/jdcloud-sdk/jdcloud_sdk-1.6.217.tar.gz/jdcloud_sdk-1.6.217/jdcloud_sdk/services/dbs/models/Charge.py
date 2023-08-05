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


class Charge(object):

    def __init__(self, chargeMode=None, chargeStatus=None, chargeStartTime=None, chargeExpiredTime=None, chargeRetireTime=None):
        """
        :param chargeMode: (Optional) 计费模式枚举值prepaid_by_duration表示预付费，postpaid_by_usage表示按用量后付费，postpaid_by_duration表示按配置后付费，默认为postpaid_by_duration
        :param chargeStatus: (Optional) 计费状态，取值为 normal表示正常，overdue表示预付费已到期，arrear表示欠费
        :param chargeStartTime: (Optional) 计费开始时间，遵循ISO8601标准，使用UTC时间，格式为：YYYY-MM-DDTHH:mm:ssZ
        :param chargeExpiredTime: (Optional) 过期时间，预付费资源的到期时间，遵循ISO8601标准，使用UTC时间，格式为：YYYY-MM-DDTHH:mm:ssZ，后付费资源此字段内容为空
        :param chargeRetireTime: (Optional) 预期释放时间，资源的预期释放时间，预付费/后付费资源均有此值，遵循ISO8601标准，使用UTC时间，格式为：YYYY-MM-DDTHH:mm:ssZ
        """

        self.chargeMode = chargeMode
        self.chargeStatus = chargeStatus
        self.chargeStartTime = chargeStartTime
        self.chargeExpiredTime = chargeExpiredTime
        self.chargeRetireTime = chargeRetireTime
