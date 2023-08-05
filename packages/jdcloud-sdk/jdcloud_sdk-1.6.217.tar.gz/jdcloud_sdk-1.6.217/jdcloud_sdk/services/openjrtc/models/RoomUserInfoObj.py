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


class RoomUserInfoObj(object):

    def __init__(self, appId=None, userRoomId=None, userId=None, nickName=None, connectId=None, status=None, joinTime=None, updateTime=None):
        """
        :param appId: (Optional) appId
        :param userRoomId: (Optional) 用户定义的房间号
        :param userId: (Optional) 业务接入方用户体系定义的且在JRTC系统内注册过的userId
        :param nickName: (Optional) 用户房间内昵称
        :param connectId: (Optional) 用户socketIo长连接id
        :param status: (Optional) 状态 1-在线 2-离线
        :param joinTime: (Optional) 创建时间
        :param updateTime: (Optional) 更新时间
        """

        self.appId = appId
        self.userRoomId = userRoomId
        self.userId = userId
        self.nickName = nickName
        self.connectId = connectId
        self.status = status
        self.joinTime = joinTime
        self.updateTime = updateTime
