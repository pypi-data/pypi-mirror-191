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


class Acl(object):

    def __init__(self, id=None, priority=None, sipType=None, sip=None, sipIpSetId=None, sipIpSetName=None, dipType=None, dip=None, dipIpSetId=None, dipIpSetName=None, protocol=None, portType=None, port=None, portSetId=None, portSetName=None, action=None, enable=None, remark=None):
        """
        :param id: (Optional) 访问控制规则 Id
        :param priority: (Optional) 规则优先级
        :param sipType: (Optional) 源IP类型: 0: IP, 1: IP地址库
        :param sip: (Optional) 源IP, sipType 为 0 时有效, 否则为空
        :param sipIpSetId: (Optional) IP地址库 Id, sipType 为 1 时有效, 否则为空。<br>'-1' IP高防回源地址<br>'-2' Web应用防火墙回源地址
        :param sipIpSetName: (Optional) IP地址库名称
        :param dipType: (Optional) 目的IP类型: 0: IP, 1: IP地址库
        :param dip: (Optional) 目的IP, dipType 为 0 时有效, 否则为空
        :param dipIpSetId: (Optional) IP地址库 Id, dipType 为 1 时有效, 否则为空。<br>'-1' IP高防回源地址<br>'-2' Web应用防火墙回源地址
        :param dipIpSetName: (Optional) IP地址库名称
        :param protocol: (Optional) 协议类型: 支持 All Traffic, TCP, UDP, ICMP
        :param portType: (Optional) 端口类型: 0: IP, 1: 端口库
        :param port: (Optional) 端口或端口范围, portType 为 0 时有效，否则为空
        :param portSetId: (Optional) 端口库Id, portType 为 1 时有效，否则为空
        :param portSetName: (Optional) 端口库名称
        :param action: (Optional) 动作: 0: 放行, 1: 阻断
        :param enable: (Optional) 规则状态: 0: 关闭, 1: 打开
        :param remark: (Optional) 备注
        """

        self.id = id
        self.priority = priority
        self.sipType = sipType
        self.sip = sip
        self.sipIpSetId = sipIpSetId
        self.sipIpSetName = sipIpSetName
        self.dipType = dipType
        self.dip = dip
        self.dipIpSetId = dipIpSetId
        self.dipIpSetName = dipIpSetName
        self.protocol = protocol
        self.portType = portType
        self.port = port
        self.portSetId = portSetId
        self.portSetName = portSetName
        self.action = action
        self.enable = enable
        self.remark = remark
