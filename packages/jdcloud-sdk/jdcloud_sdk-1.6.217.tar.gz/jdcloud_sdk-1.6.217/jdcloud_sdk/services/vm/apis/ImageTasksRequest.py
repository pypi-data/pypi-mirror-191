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

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class ImageTasksRequest(JDCloudRequest):
    """
    
查询镜像任务详情。

将京东云私有镜像导出至京东云以外环境。

详细操作说明请参考帮助文档：
[导入私有镜像](https://docs.jdcloud.com/cn/virtual-machines/import-private-image)
[导出私有镜像](https://docs.jdcloud.com/cn/virtual-machines/export-private-image)

## 接口说明
- 调用该接口可查询镜像导入或导出的任务详情。

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ImageTasksRequest, self).__init__(
            '/regions/{regionId}/imageTasks', 'GET', header, version)
        self.parameters = parameters


class ImageTasksParameters(object):

    def __init__(self,regionId, ):
        """
        :param regionId: 地域ID。
        """

        self.regionId = regionId
        self.taskAction = None
        self.taskIds = None
        self.taskStatus = None
        self.startTime = None
        self.endTime = None
        self.pageNumber = None
        self.pageSize = None

    def setTaskAction(self, taskAction):
        """
        :param taskAction: (Optional) 任务操作类型。支持范围：`ImportImage、ExportImage`。
        """
        self.taskAction = taskAction

    def setTaskIds(self, taskIds):
        """
        :param taskIds: (Optional) 任务id列表。
        """
        self.taskIds = taskIds

    def setTaskStatus(self, taskStatus):
        """
        :param taskStatus: (Optional) 任务状态。支持范围：`pending、running、failed、finished`。
        """
        self.taskStatus = taskStatus

    def setStartTime(self, startTime):
        """
        :param startTime: (Optional) 任务开始时间
        """
        self.startTime = startTime

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 任务结束时间
        """
        self.endTime = endTime

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 页码；默认为1。
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 分页大小；取值范围[10, 100]。
        """
        self.pageSize = pageSize

