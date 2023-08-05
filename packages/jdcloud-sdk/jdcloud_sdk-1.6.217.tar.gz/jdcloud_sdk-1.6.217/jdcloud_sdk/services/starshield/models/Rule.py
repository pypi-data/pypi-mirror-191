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


class Rule(object):

    def __init__(self, id=None, enabled=None, version=None, description=None, expression=None, action=None, action_parameters=None, ratelimit=None):
        """
        :param id: (Optional) 规则的标识。
        :param enabled: (Optional) 是否开启规则，有效值true/false。
        :param version: (Optional) 规则的版本。
        :param description: (Optional) 规则的描述。
        :param expression: (Optional) 表达式。
UI字段==============API字段==================UI运算符================================================================
ASN----------------ip.geoip.asnum----------------------等于/不等于/大于/小于/大于或等于/小于或等于/包含以下各项/不包含以下各项
Cookie-------------http.cookie-------------------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
国家/地区-----------ip.geoip.country--------------------等于/不等于/包含以下各项/不包含以下各项
洲-----------------ip.geoip.continent------------------等于/不等于/包含以下各项/不包含以下各项
主机名--------------http.host---------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配/包含以下各项/不包含以下各项
IP源地址------------ip.src------------------------------等于/不等于/包含以下各项/不包含以下各项/在列表中/不在列表中
引用方--------------http.referer------------------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
请求方法------------http.request.method------------------等于/不等于/包含以下各项/不包含以下各项
URI完整------------http.request.full_uri----------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
URI----------------http.request.uri--------------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
URI路径-------------http.request.uri.path----等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配/包含以下各项/不包含以下各项
URI查询字符串--------http.request.uri.query--------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
HTTP版本------------http.request.version----------------等于/不等于/包含以下各项/不包含以下各项
用户代理-------------http.user_agent---------------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
X-Forwarded-For----http.x_forwarded_for----------------等于/不等于/包含/不包含/与正则表达式匹配/与正则表达式不匹配
合法机器人爬虫--------cf.client.bot
威胁分数-------------cf.threat_score---------------------等于/不等于/大于/小于/大于或等于/小于或等于/包含以下各项/不包含以下各项
已通过验证的自动程序---cf.bot_management.verified_bot
自动程序分数----------cf.bot_management.score-------------等于/不等于/大于/小于/大于或等于/小于或等于/包含以下各项/不包含以下各项
自动程序JS分数--------cf.bot_management.js_score----------等于/不等于/大于/小于/大于或等于/小于或等于/包含以下各项/不包含以下各项
提供静态资源----------cf.bot_management.static_resource
JA3指纹--------------cf.bot_management.ja3_hash----------等于/不等于

UI运算符============================API运算符
等于-------------------------------eq
不等于-----------------------------ne
大于-------------------------------gt
小于-------------------------------lt
大于或等于--------------------------ge
小于或等于--------------------------le
在列表中----------------------------
不在列表中--------------------------
包含-------------------------------contains
不包含-----------------------------not <x> contains，例如：not http.x_forwarded_for contains
与正则表达式匹配---------------------matches
与正则表达式不匹配--------------------not <x> matches，例如：not http.user_agent matches
包含以下各项-------------------------in
不包含以下各项-----------------------not <x> in，例如：not cf.bot_management.js_score in

        :param action: (Optional) 当表达式匹配时，采取的措施。有效值block/challenge/js_challenge/managed_challenge/log。
        :param action_parameters: (Optional) 
        :param ratelimit: (Optional) 规则中的速率限制规则。
        """

        self.id = id
        self.enabled = enabled
        self.version = version
        self.description = description
        self.expression = expression
        self.action = action
        self.action_parameters = action_parameters
        self.ratelimit = ratelimit
