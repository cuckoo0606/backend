# !/usr/lib/env python
# -*- encoding:utf-8 -*-

# Auhtor: cuckoo
# Email: skshadow0606@gmail.com
# Create Date: 2017-10-19 16:12:25

ERROR_CODES = {
    # GLOBAL
    "PERMISSION_DENIED": "权限错误",
    "UNKNOW_ERROR": "未知错误",
    "NAME_NOT_NONE": "名称不能为空",
    "RECORD_NOT_EXIST": "记录不存在",
    "ID_NOT_NONE": "标识码不能为空",
    "NO_CHOOSE_ITEMS": "未选择数据",
    "BE_ASSOCIATED": "已被关联, 不能删除",
    "SOME_BE_ASSOCIATED": "只能删除未被关联的数据",
    "TITLE_NOT_NONE": "标题不能为空",
    "VALUE_MUST_BE_GREATER_THAN_ZERO": "数值必须大于0",
    "FORMAT_IS_WRONG": "格式有误",
    "SETUP_FAILED": "设置失败",

    # Commodity
    "CLASSIFICATION_NOT_NONE": "商品分类还没选择",
    "OPEN_TIME_ERROR": "开放时间格式有误",
    "CONTENT_NOT_NONE": "内容不能为空",
    "TRADE_MODE_NOT_NONE": "交易模式不能为空",
    "STATUS_CODE_NOT_NONE": "状态码不能为空",
    "CYCLE_ARGS_ERROR": "周期参数错误",
    "CYCLE_TIME_ERROR": "周期时间参数错误",
    "CYCLE_IN_ERROR": "周期价内参数错误",
    "CYCLE_OUT_ERROR": "周期价外参数错误",
    "CYCLE_PRICE_ERROR": "周期价格格式错误",
    "CYCLE_ARGS_NOT_NONE": "周期参数不可留空",
    "LIMIT_MUST_INT": "投资额度必须为整数",

    # Fundsflow
    "UNCHECK_PAYEE": "未选中收款人",
    "NOT_FOUND_PAYEE": "未找到收款人",
    "USER_CANNOT_OUT_GOLD": "此用户无法出金",
    "AMOUNT_CANNOT_0": "充值金额不能为0",
    "INVALID_FORMAT_AMOUNT": "金额格式错误",
    "GOLD_TIME_ERROR": "当前时间不在出金时间内",
    "NOT_FOUND_GOLD": "未找到出金人",
    "AMOUNT_MUST_BE_GREATER_THAN_ZERO": "金额必须大于0",
    "GOLD_PEOPLE_DONOT_HAVE_ENOUGH_BALANCE": "出金人余额不足",
    "GOLD_BEYOND_LIMIT": "支付方当天出金超出限额",
    "USER_EXCEPTION": "用户异常",
    "BANK_INFO_IS_NOT_COMPLETE": "银行信息不全",
    "DOES_NOT_SUPPORT_BANK": "暂不支持此银行",
    "BANKID_NOT_NONE": "开户行行号不能为空",
    "MERCHANTS_UNKNOWN": "未明的商户",
    "ABNORMAL_ORDERS": "订单异常",
    "CANNOT_BATCH_PROCESSING": "线上出金模式不能批量处理",

    # Permission
    "IDENTIFY_EXISTING": "此标识已存在",
    "ID_CANNOT_BE_MODIFIED": "标识码不能修改",
    "ROLE_DID_NOT_CHOOSE": "角色未选择",
    "ROLE_AUTHORIZATION_CANNOT_BE_EMPTY": "权限不能为空",

    # System
    "INVALID_FORMAT": "格式错误",
    "MUST_BE_INT": "必须为整数",
    "USER_GROUP_ERROR": "用户组有误",
    "REFEREE_ERROR": "没有此推荐人",
    "PARAMETER_IS_NOT_COMPLETE": "参数不全",

    # User
    "CHARACTER_CANNOT_BE_EMPTY": "用户角色不能为空",
    "PWD_CANNOT_BE_EMPTY": "密码不能为空",
    "PHONE_CANNOT_BE_EMPTY": "手机号码不能为空",
    "PHONE_FORMAT_ERROR": "手机号码格式有误",
    "USERID_FORMAT_ERROR": "注册名不符合规则",
    "BANK_ACCOUNT_FORMAT_ERROR": "银行账号格式错误",
    "USER_ID_ALREADY_EXIST": "用户标识已存在",
    "TOTAL_DISH_FORMAT_IS_WRONG": "总盘口格式有误",
    "IDENTIFIER_ONLY": "标识码唯一",
    "DO_NOT_CHANGE_THEIR_OWN_ROLES": "不可更改自己的角色",
    "ADMINISTRATOR_ROLE_CANNOT_BE_CHANGED": "管理员角色不可更改",
    "CHARACTER_CANNOT_BE_CHANGED_AS_ADMINISTRATOR": "角色不可更改为管理员",
    "NO_PERMISSION_TO_CHANGE_ROLE": "无权限更改角色",
    "WITHOUT_THIS_AGENT": "无此代理商用户id, 无法绑定上级",
    "WITHOUT_THIS_USER_GROUP": "没有此用户组",
    "ODDS_FORMAT_ERROR": "比例设置格式错误",
    "NUMERIC_ERROR": "最大值要大于最小值",
    "NUMERIC_FORMAT_ERROR": "最大值或最小值不合法",
    "TYPE_ERROR": "用户类型异常",
    "PERMISSIONS_FAILURE": "不能设置非一下级的用户",
    "": "不能修改自己的佣金",
    "CANNOT_MODIFY_THEIR_OWN": "不能修改自己的数值",

    # Api
    "ARG_ERROR": "传入的参数有误"
}


def error_code(code):
    '''
        Return an error code in the form of a dictionary.
    '''
    return {"status": "faild", "desc": ERROR_CODES[code]}
