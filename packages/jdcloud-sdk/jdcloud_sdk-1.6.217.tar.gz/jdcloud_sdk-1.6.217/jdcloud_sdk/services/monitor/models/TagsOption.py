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


class TagsOption(object):

    def __init__(self, operator=None, tags=None):
        """
        :param operator: (Optional) 操作项(多个tagFilter之间关关系)默认是or
        :param tags: (Optional) 资源标签,对所有符合该标签的资源设置报警规则，对于新加入该标签的资源自动生效
        """

        self.operator = operator
        self.tags = tags
