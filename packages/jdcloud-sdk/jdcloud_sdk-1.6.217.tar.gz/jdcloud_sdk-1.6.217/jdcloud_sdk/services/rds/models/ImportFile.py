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


class ImportFile(object):

    def __init__(self, name=None, sharedFileGid=None, sizeByte=None, uploadTime=None, isLocal=None, status=None, importTime=None):
        """
        :param name: (Optional) 文件名称
        :param sharedFileGid: (Optional) 如果该文件是共享文件，则有全局ID，如不是共享文件，则为空。该全局ID在文件删除时，需要用到
        :param sizeByte: (Optional) 文件大小，单位Byte
        :param uploadTime: (Optional) 文件上传完成时间，格式为：YYYY-MM-DD HH:mm:ss
        :param isLocal: (Optional) 是否所属当前实例.<br> 1：当前实例；<br>0：不是当前实例，为共享文件
        :param status: (Optional) 文件状态<br>- 仅支持SQL Server
        :param importTime: (Optional) 导入完成时间,格式为：YYYY-MM-DD HH:mm:ss<br>- 仅支持SQL Server
        """

        self.name = name
        self.sharedFileGid = sharedFileGid
        self.sizeByte = sizeByte
        self.uploadTime = uploadTime
        self.isLocal = isLocal
        self.status = status
        self.importTime = importTime
