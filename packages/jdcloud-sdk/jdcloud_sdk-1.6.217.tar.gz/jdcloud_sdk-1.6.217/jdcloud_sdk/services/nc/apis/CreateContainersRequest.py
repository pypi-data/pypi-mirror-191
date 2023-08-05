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


class CreateContainersRequest(JDCloudRequest):
    """
    创建一台或多台指定配置容器。
- 创建容器需要通过实名认证
- 镜像
    - 容器的镜像通过镜像名称来确定
    - nginx:tag 或 mysql/mysql-server:tag 这样命名的镜像表示 docker hub 官方镜像
    - container-registry/image:tag 这样命名的镜像表示私有仓储的镜像
    - 私有仓储必须兼容 docker registry 认证机制，并通过 secret 来保存机密信息
- hostname 规范
    - 支持两种方式：以标签方式书写或以完整主机名方式书写
    - 标签规范
        - 0-9，a-z(不分大小写)和 -（减号），其他的都是无效的字符串
        - 不能以减号开始，也不能以减号结尾
        - 最小1个字符，最大63个字符
    - 完整的主机名由一系列标签与点连接组成
        - 标签与标签之间使用“.”(点)进行连接
        - 不能以“.”(点)开始，也不能以“.”(点)结尾
        - 整个主机名（包括标签以及分隔点“.”）最多有63个ASCII字符
- 网络配置
    - 指定主网卡配置信息
        - 必须指定一个子网
        - 一台云主机创建时必须指定一个安全组，至多指定 5 个安全组
        - 可以指定 elasticIp 规格来约束创建的弹性 IP，带宽取值范围 [1-200]Mbps，步进 1Mbps
        - 可以指定网卡的主 IP(primaryIpAddress)，该 IP 需要在子网 IP 范围内且未被占用，指定子网 IP 时 maxCount 只能为1
        - 安全组 securityGroup 需与子网 Subnet 在同一个私有网络 VPC 内
        - 主网卡 deviceIndex 设置为 1
- 存储
    - volume 分为 root volume 和 data volume，root volume 的挂载目录是 /，data volume 的挂载目录可以随意指定
    - volume 的底层存储介质当前只支持 cloud 类别，也就是云硬盘
    - 系统盘
        - 云硬盘类型可以选择 ssd、premium-hdd
        - 磁盘大小
            - ssd：范围 [10, 100]GB，步长为 10G
            - premium-hdd：范围 [20, 1000]GB，步长为 10G
        - 自动删除
            - 云盘默认跟随容器实例自动删除，如果是包年包月的数据盘或共享型数据盘，此参数不生效
        - 可以选择已存在的云硬盘
    - 数据盘
        - 云硬盘类型可以选择 ssd、premium-hdd
        - 磁盘大小
            - ssd：范围[20,1000]GB，步长为10G
            - premium-hdd：范围[20,3000]GB，步长为10G
        - 自动删除
            - 默认自动删除
        - 可以选择已存在的云硬盘
        - 单个容器最多可以挂载 7 个 data volume
- 计费
  - 弹性IP的计费模式，如果选择按用量类型可以单独设置，其它计费模式都以主机为准
  - 云硬盘的计费模式以主机为准
- 容器日志
    - 默认在本地分配10MB的存储空间，自动 rotate
- 其他
    - 创建完成后，容器状态为running
    - maxCount 为最大努力，不保证一定能达到 maxCount

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateContainersRequest, self).__init__(
            '/regions/{regionId}/containers', 'POST', header, version)
        self.parameters = parameters


class CreateContainersParameters(object):

    def __init__(self, regionId, ):
        """
        :param regionId: Region ID
        """

        self.regionId = regionId
        self.containerSpec = None
        self.maxCount = None

    def setContainerSpec(self, containerSpec):
        """
        :param containerSpec: (Optional) 创建容器规格
        """
        self.containerSpec = containerSpec

    def setMaxCount(self, maxCount):
        """
        :param maxCount: (Optional) 购买实例数量；取值范围：[1,100]
        """
        self.maxCount = maxCount

