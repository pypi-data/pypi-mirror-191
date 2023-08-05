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


class InstanceNetworkInterfaceAttachment(object):

    def __init__(self, autoDelete=None, deviceIndex=None, attachStatus=None, attachTime=None, networkInterface=None):
        """
        :param autoDelete: (Optional) 指明删除实例时是否删除网卡
        :param deviceIndex: (Optional) 设备Index，暂不提供辅助网卡index
        :param attachStatus: (Optional) 绑定状态
        :param attachTime: (Optional) 绑定时间
        :param networkInterface: (Optional) 弹性网卡信息
        """

        self.autoDelete = autoDelete
        self.deviceIndex = deviceIndex
        self.attachStatus = attachStatus
        self.attachTime = attachTime
        self.networkInterface = networkInterface
