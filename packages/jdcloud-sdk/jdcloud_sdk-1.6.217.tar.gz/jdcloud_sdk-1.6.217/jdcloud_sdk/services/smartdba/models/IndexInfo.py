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


class IndexInfo(object):

    def __init__(self, indexName=None, db=None, tableName=None):
        """
        :param indexName: (Optional) 索引名称
        :param db: (Optional) 库名
        :param tableName: (Optional) 表名
        """

        self.indexName = indexName
        self.db = db
        self.tableName = tableName
