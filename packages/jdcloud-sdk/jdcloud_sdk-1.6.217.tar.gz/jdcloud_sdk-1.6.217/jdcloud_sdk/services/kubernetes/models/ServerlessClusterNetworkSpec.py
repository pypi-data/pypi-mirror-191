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


class ServerlessClusterNetworkSpec(object):

    def __init__(self, publicApiServer=None, masterCidr=None, vpcId=None, natGateway=None, serviceCidr=None, podSubnetId=None, lbSubnetId=None, dualStack=None, masterNatEnabled=None):
        """
        :param publicApiServer: (Optional) kube-apiserver是否可公网访问，false则kube-apiserver不绑定公网地址，true绑定公网地址
        :param masterCidr: (Optional) master子网CIDR
        :param vpcId: (Optional) Pod所在VPC
        :param natGateway: (Optional) 
        :param serviceCidr: (Optional) service所在子网CIDR
        :param podSubnetId: (Optional) pod所在子网ID
        :param lbSubnetId: (Optional) lb所在子网ID
        :param dualStack: (Optional) 是否双栈支持，开启后，kube-apiserver将拥有ipv6地址，默认不开启
        :param masterNatEnabled: (Optional) 是否开启master访问公网的能力，如果需要引入公网OIDC认证时需要开启，默认不开启
        """

        self.publicApiServer = publicApiServer
        self.masterCidr = masterCidr
        self.vpcId = vpcId
        self.natGateway = natGateway
        self.serviceCidr = serviceCidr
        self.podSubnetId = podSubnetId
        self.lbSubnetId = lbSubnetId
        self.dualStack = dualStack
        self.masterNatEnabled = masterNatEnabled
