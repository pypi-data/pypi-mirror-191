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


class ProductServiceVo(object):

    def __init__(self, deliverNumber=None, orderNumber=None, refOrderNumber=None, orderType=None, orderTypeName=None, buyerPin=None, mappingCode=None, supportAutoDeliver=None, productId=None, skuId=None, skuName=None, serviceCode=None, num=None, period=None, periodType=None, periodTypeName=None, accountNum=None, deliverStatus=None, deliverStatusName=None, effectiveDt=None, failureDt=None, extraInfo=None, remark=None, orderTotalFee=None, orderActualFee=None, paymentDt=None, extraChargeInfo=None, orderItemExtraChargeInfos=None):
        """
        :param deliverNumber: (Optional) 交付单号
        :param orderNumber: (Optional) 订单号
        :param refOrderNumber: (Optional) 续费订单所关联的新购订单号，该字段只针对续费单有效，新购单该字段为null
        :param orderType: (Optional) 订单类型
        :param orderTypeName: (Optional) 订单类型名称
        :param buyerPin: (Optional) 购买人
        :param mappingCode: (Optional) 映射编号
        :param supportAutoDeliver: (Optional) 是否支持自动交付：0表示不支持，1表示支持
        :param productId: (Optional) 产品ID
        :param skuId: (Optional) sku ID
        :param skuName: (Optional) sku名称
        :param serviceCode: (Optional) 服务code
        :param num: (Optional) 数量
        :param period: (Optional) 周期
        :param periodType: (Optional) 周期类型
        :param periodTypeName: (Optional) 周期类型名称
        :param accountNum: (Optional) 账号数量
        :param deliverStatus: (Optional) 交付状态
        :param deliverStatusName: (Optional) 交付状态名称
        :param effectiveDt: (Optional) 服务生效时间，格式：yyyy-MM-dd HH:mm:ss
        :param failureDt: (Optional) 服务过期时间，格式：yyyy-MM-dd HH:mm:ss
        :param extraInfo: (Optional) 商品属性
        :param remark: (Optional) 交付单备注
        :param orderTotalFee: (Optional) 订单金额
        :param orderActualFee: (Optional) 订单实付金额
        :param paymentDt: (Optional) 订单支付时间
        :param extraChargeInfo: (Optional) 额外计费项信息
        :param orderItemExtraChargeInfos: (Optional) 额外计费详情信息
        """

        self.deliverNumber = deliverNumber
        self.orderNumber = orderNumber
        self.refOrderNumber = refOrderNumber
        self.orderType = orderType
        self.orderTypeName = orderTypeName
        self.buyerPin = buyerPin
        self.mappingCode = mappingCode
        self.supportAutoDeliver = supportAutoDeliver
        self.productId = productId
        self.skuId = skuId
        self.skuName = skuName
        self.serviceCode = serviceCode
        self.num = num
        self.period = period
        self.periodType = periodType
        self.periodTypeName = periodTypeName
        self.accountNum = accountNum
        self.deliverStatus = deliverStatus
        self.deliverStatusName = deliverStatusName
        self.effectiveDt = effectiveDt
        self.failureDt = failureDt
        self.extraInfo = extraInfo
        self.remark = remark
        self.orderTotalFee = orderTotalFee
        self.orderActualFee = orderActualFee
        self.paymentDt = paymentDt
        self.extraChargeInfo = extraChargeInfo
        self.orderItemExtraChargeInfos = orderItemExtraChargeInfos
