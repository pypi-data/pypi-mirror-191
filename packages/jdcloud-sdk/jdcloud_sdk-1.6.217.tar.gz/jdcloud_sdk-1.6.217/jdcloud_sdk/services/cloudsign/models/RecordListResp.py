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


class RecordListResp(object):

    def __init__(self, number=None, last=None, numberOfElements=None, size=None, totalPages=None, first=None, empty=None, totalElements=None, content=None):
        """
        :param number: (Optional) 当前是第几页，page
        :param last: (Optional) 是否是最后一页
        :param numberOfElements: (Optional) 当前页数量
        :param size: (Optional) 每页数量
        :param totalPages: (Optional) 总共多少页
        :param first: (Optional) 是否第一页
        :param empty: (Optional) 是否为空
        :param totalElements: (Optional) 总数目
        :param content: (Optional) 
        """

        self.number = number
        self.last = last
        self.numberOfElements = numberOfElements
        self.size = size
        self.totalPages = totalPages
        self.first = first
        self.empty = empty
        self.totalElements = totalElements
        self.content = content
