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


class CreateSgRule(object):

    def __init__(self, ruleType, protocol, fromPort, toPort, securityGroupId, cidrIp, nicType=None, policy=None, priority=None):
        """
        :param ruleType:  规则类型，ingress、egress
        :param protocol:  协议，tcp、udp、icmp 或者 all
        :param fromPort:  起始端口
        :param toPort:  终止端口
        :param securityGroupId:  安全组ID
        :param nicType: (Optional) 网络类型，internet、intranet
        :param policy: (Optional) 认证策略，accept、drop
        :param priority: (Optional) 认证策略的权重，1-100。
        :param cidrIp:  目标IP地址范围
        """

        self.ruleType = ruleType
        self.protocol = protocol
        self.fromPort = fromPort
        self.toPort = toPort
        self.securityGroupId = securityGroupId
        self.nicType = nicType
        self.policy = policy
        self.priority = priority
        self.cidrIp = cidrIp
