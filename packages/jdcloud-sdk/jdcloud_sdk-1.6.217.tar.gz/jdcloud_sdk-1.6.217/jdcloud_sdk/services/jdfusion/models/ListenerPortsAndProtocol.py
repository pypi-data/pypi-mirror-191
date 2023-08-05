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


class ListenerPortsAndProtocol(object):

    def __init__(self, listenerPort=None, listenerProtocol=None, listenerForward=None, forwardPort=None):
        """
        :param listenerPort: (Optional) 负载均衡实例前端使用的端口。
        :param listenerProtocol: (Optional) 负载均衡实例前端使用的协议。
        :param listenerForward: (Optional) 是否启用监听转发。
        :param forwardPort: (Optional) 转发到的目的监听端口，必须是已经存在的HTTPS监听端口。
        """

        self.listenerPort = listenerPort
        self.listenerProtocol = listenerProtocol
        self.listenerForward = listenerForward
        self.forwardPort = forwardPort
