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


class JDCloudVolumeSource(object):

    def __init__(self, volumeId=None, snapshotId=None, diskType=None, sizeGB=None, fsType=None, formatVolume=None, iops=None, autoDelete=None):
        """
        :param volumeId: (Optional) 云盘id，使用已有云盘
        :param snapshotId: (Optional) 云盘快照id，根据云盘快照创建云盘。
        :param diskType: (Optional) 云盘类型：hdd.std1,ssd.gp1,ssd.io1
        :param sizeGB: (Optional) 云盘size,单位 GB,要求
        :param fsType: (Optional) 指定volume文件系统类型，目前支持[xfs, ext4]；如果新创建的盘，不指定文件系统类型默认格式化成xfs
        :param formatVolume: (Optional) 随容器自动创建的新盘，会自动格式化成指定的文件系统类型；挂载已有的盘，默认不会格式化，只会按照指定的fsType去挂载；如果希望格式化，必须设置此字段为true
        :param iops: (Optional) 云盘的 iops 值，目前只有 ssd.io1 类型有效
        :param autoDelete: (Optional) 是否随pod删除。默认：true
        """

        self.volumeId = volumeId
        self.snapshotId = snapshotId
        self.diskType = diskType
        self.sizeGB = sizeGB
        self.fsType = fsType
        self.formatVolume = formatVolume
        self.iops = iops
        self.autoDelete = autoDelete
