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


class ServerlessMasterVersion(object):

    def __init__(self, version=None, isDefault=None, versionStatus=None, clusterAddons=None):
        """
        :param version: (Optional) 版本号
        :param isDefault: (Optional) 是否默认版本
        :param versionStatus: (Optional) 版本状态
        :param clusterAddons: (Optional) 该版本可以安装的组件列表
        """

        self.version = version
        self.isDefault = isDefault
        self.versionStatus = versionStatus
        self.clusterAddons = clusterAddons
