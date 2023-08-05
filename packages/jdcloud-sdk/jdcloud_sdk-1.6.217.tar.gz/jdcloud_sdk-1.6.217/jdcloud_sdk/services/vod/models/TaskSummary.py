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


class TaskSummary(object):

    def __init__(self, taskId=None, snapshotType=None, status=None, errorCode=None, errorMessage=None, createTime=None, updateTime=None):
        """
        :param taskId: (Optional) 任务ID
        :param snapshotType: (Optional) 模板类型。取值范围：
  sample - 采样截图模板
  sprite - 雪碧图模板

        :param status: (Optional) 任务状态。
- submitted
- processing
- succeeded
- failed

        :param errorCode: (Optional) 错误码
        :param errorMessage: (Optional) 错误信息
        :param createTime: (Optional) 创建时间
        :param updateTime: (Optional) 修改时间
        """

        self.taskId = taskId
        self.snapshotType = snapshotType
        self.status = status
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.createTime = createTime
        self.updateTime = updateTime
