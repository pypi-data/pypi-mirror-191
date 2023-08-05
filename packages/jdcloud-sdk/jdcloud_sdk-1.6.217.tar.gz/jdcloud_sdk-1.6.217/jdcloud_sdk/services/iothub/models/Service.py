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


class Service(object):

    def __init__(self, name=None, serviceId=None, description=None, input=None, output=None, code=None, createdTime=None):
        """
        :param name: (Optional) 服务名称
        :param serviceId: (Optional) 服务ID
        :param description: (Optional) 服务描述
        :param input: (Optional) 服务入参,object的key为参数名称，value为参数值
        :param output: (Optional) 服务出参,object的key为参数名称，value为参数值
        :param code: (Optional) 结果码200:成功,400:参数错误
        :param createdTime: (Optional) 创建时间
        """

        self.name = name
        self.serviceId = serviceId
        self.description = description
        self.input = input
        self.output = output
        self.code = code
        self.createdTime = createdTime
