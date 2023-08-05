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


class DBInstance(object):

    def __init__(self, instanceId=None, instanceName=None, nodeType=None, cpu=None, memory=None, storage=None, nodeNumber=None, azId=None, vpcId=None, subnetId=None, instanceStatus=None, createTime=None, charge=None):
        """
        :param instanceId: (Optional) 实例ID
        :param instanceName: (Optional) 实例名称
        :param nodeType: (Optional) 节点规格
        :param cpu: (Optional) CPU核数
        :param memory: (Optional) 内存容量，单位GB
        :param storage: (Optional) 存储空间容量，单位GB
        :param nodeNumber: (Optional) 节点数量
        :param azId: (Optional) 可用区
        :param vpcId: (Optional) VPCID
        :param subnetId: (Optional) 子网ID
        :param instanceStatus: (Optional) 实例状态
        :param createTime: (Optional) 创建时间
        :param charge: (Optional) 计费配置
        """

        self.instanceId = instanceId
        self.instanceName = instanceName
        self.nodeType = nodeType
        self.cpu = cpu
        self.memory = memory
        self.storage = storage
        self.nodeNumber = nodeNumber
        self.azId = azId
        self.vpcId = vpcId
        self.subnetId = subnetId
        self.instanceStatus = instanceStatus
        self.createTime = createTime
        self.charge = charge
