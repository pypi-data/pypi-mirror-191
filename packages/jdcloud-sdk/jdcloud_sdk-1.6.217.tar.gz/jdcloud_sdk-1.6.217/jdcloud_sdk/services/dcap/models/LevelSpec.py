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


class LevelSpec(object):

    def __init__(self, levelId=None, levelTag=None, levelDesc=None):
        """
        :param levelId: (Optional) 敏感数据等级
1. 值越大，敏感等级越高
2. 最小值为0

        :param levelTag: (Optional) 敏感数据标签
        :param levelDesc: (Optional) 敏感数据描述
        """

        self.levelId = levelId
        self.levelTag = levelTag
        self.levelDesc = levelDesc
