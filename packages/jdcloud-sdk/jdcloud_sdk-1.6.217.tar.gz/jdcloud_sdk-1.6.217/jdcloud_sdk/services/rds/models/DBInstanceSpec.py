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


class DBInstanceSpec(object):

    def __init__(self, engine, engineVersion, instanceClass, instanceStorageGB, azId, vpcId, subnetId, chargeSpec, instanceName=None, parameterGroup=None, instanceStorageType=None, instancePort=None, storageEncrypted=None, instanceType=None, tagSpec=None):
        """
        :param instanceName: (Optional) 实例名，具体规则可参见帮助中心文档:[名称及密码限制](../../../documentation/Database-and-Cache-Service/RDS/Introduction/Restrictions/SQLServer-Restrictions.md)
        :param engine:  实例引擎类型，参见[枚举参数定义](../Enum-Definitions/Enum-Definitions.md)
        :param engineVersion:  实例引擎版本，参见[枚举参数定义](../Enum-Definitions/Enum-Definitions.md)
        :param instanceClass:  实例规格代码，可以查看文档[MySQL 实例规格](../Instance-Specifications/Instance-Specifications-MySQL.md)、[SQL Server实例规格](../Instance-Specifications/Instance-Specifications-SQLServer.md)
        :param instanceStorageGB:  磁盘大小，单位GB，可以查看文档[MySQL 实例规格](../Instance-Specifications/Instance-Specifications-MySQL.md)、[SQL Server实例规格](../Instance-Specifications/Instance-Specifications-SQLServer.md)
        :param azId:  可用区ID， 第一个ID必须为主实例所在的可用区。如两个可用区一样，也需输入两个azId
        :param vpcId:  VPC的ID
        :param subnetId:  子网ID
        :param parameterGroup: (Optional) 参数组ID, 缺省系统会创建一个默认参数组<br>- 仅支持MySQL
        :param chargeSpec:  计费规格，包括计费类型，计费周期等
        :param instanceStorageType: (Optional) 存储类型，参见[枚举参数定义](../Enum-Definitions/Enum-Definitions.md), 缺省值为：LOCAL_SSD<br>- 仅支持MySQL
        :param instancePort: (Optional) 应用访问端口，支持的端口范围：1150～5999。MySQL、Percona、MariaDB的默认值为 3306；SQL SQL Server的默认值为1433，不支持5022；PostgreSQL的默认端口号为5432；
        :param storageEncrypted: (Optional) 实例数据加密(存储类型为云硬盘才支持数据加密)。false：不加密，true：加密，缺省为false<br>- 仅支持MySQL
        :param instanceType: (Optional) 实例的高可用架构。standalone：单机，cluster：主备双机架构，缺省为cluster<br>- 仅支持SQL Server
        :param tagSpec: (Optional) 标签信息
        """

        self.instanceName = instanceName
        self.engine = engine
        self.engineVersion = engineVersion
        self.instanceClass = instanceClass
        self.instanceStorageGB = instanceStorageGB
        self.azId = azId
        self.vpcId = vpcId
        self.subnetId = subnetId
        self.parameterGroup = parameterGroup
        self.chargeSpec = chargeSpec
        self.instanceStorageType = instanceStorageType
        self.instancePort = instancePort
        self.storageEncrypted = storageEncrypted
        self.instanceType = instanceType
        self.tagSpec = tagSpec
