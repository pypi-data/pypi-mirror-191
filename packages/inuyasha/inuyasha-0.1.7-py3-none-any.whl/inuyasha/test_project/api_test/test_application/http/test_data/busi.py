from pytest_cases import case, parametrize

from utils.data_utils.single_interface.strategy import Strategy


class BusinessIsignCardbin:
    s = Strategy()

    @case(tags=['业务逻辑测试', '商户状态校验'])
    @parametrize(mch_id=(
            {"正常状态商户号": {"mch_id": "302207190000043504"}},
            {"异常状态商户号": {"mch_id": "302208100000044473"}},
            {"商户未订购快捷产品": {"mch_id": "302208100000044365"}},
            {"商户IP非白名单": {"mch_id": "302208100000044470"}},
            {"商户不存在": {"mch_id": "302207190000043502"}},
    ))
    def business_sign_carbin_mch_state(self, mch_id):
        return list(mch_id.values())[0]

    @case(tags=['业务逻辑测试', '签约状态校验'])
    @parametrize(data=(
            {"用户未签约": {"user_id": "943640699113", "card_no": "6222625295206823159"}},
            {"用户已签约": {"user_id": "943640699112", "card_no": "6222625295206823158"}},
            {"用户已解约": {"user_id": "948414554411", "card_no": "6222625295206396846"}},
    ))
    def business_sign_carbin_sign_state(self, data):
        template = {
            "mch_id": "302207190000043504",
        }
        template.update(list(data.values())[0])
        return template


class BusinessIsignQuery:
    s = Strategy()

    @case(tags=['业务逻辑测试', '商户状态校验'])
    @parametrize(mch_id=(
            {"正常状态商户号": {"mch_id": "302207190000043504"}},
            {"异常状态商户号": {"mch_id": "302208100000044473"}},
            {"商户未订购快捷产品": {"mch_id": "302208100000044365"}},
            {"商户IP非白名单": {"mch_id": "302208100000044470"}},
            {"商户不存在": {"mch_id": "302207190000043502"}},
    ))
    def business_sign_query_mch_state(self, mch_id):
        return list(mch_id.values())[0]

    @case(tags=['业务逻辑测试', '签约状态校验'])
    @parametrize(data=(
            {"用户未签约": {"user_id": "943640699113"}},
            {"用户已签约": {"user_id": "943640699112"}},
            {"用户已解约": {"user_id": "948414554411"}},
    ))
    def business_sign_query_sign_state(self, data):
        template = {
            "mch_id": "302207190000043504",
        }
        template.update(list(data.values())[0])
        return template


class BusinessIsignApply:
    s = Strategy()

    @case(tags=['业务逻辑测试', '商户状态校验'])
    @parametrize(mch_id=(
            {"正常状态商户号": {"mch_id": "302207190000043504"}},
            {"异常状态商户号": {"mch_id": "302208100000044473"}},
            {"商户未订购快捷产品": {"mch_id": "302208100000044365"}},
            {"商户IP非白名单": {"mch_id": "302208100000044470"}},
            {"商户不存在": {"mch_id": "302207190000043502"}},
    ))
    def business_sign_apply_mch_state(self, mch_id):
        return list(mch_id.values())[0]

    @case(tags=['业务逻辑测试', '签约状态校验'])
    @parametrize(data=(
            {"用户首次申请签约": {}},
            {"用户已签约再次申请": {"user_id": "943640699112", "card_no": "6222625295206823158", "id_no": "610825199105181174", "acct_name": "杨桂英", "bind_phone": "18695294724"}},
            {"用户已签约再次申请仅手机号不同": {"user_id": "943640699112", "card_no": "6222625295206823158", "id_no": "610825199105181174", "acct_name": "杨桂英"}},
            {"用户已解约再次申请数据相同": {"user_id": "948414554411", "card_no": "6222625295206396846", "id_no": "440704193602249751", "acct_name": "乌勇", "bind_phone": "13494229122"}},
    ))
    def business_sign_apply_sign_state(self, data):
        template = {
            "mch_id": "302207190000043504",
        }
        template.update(list(data.values())[0])
        return template


class BusinessIsignVerify:
    s = Strategy()

    @case(tags=['业务逻辑测试', '商户状态校验'])
    @parametrize(mch_id=(
            {"异常状态商户号": {"mch_id": "302208100000044473"}},
            # {"商户未订购快捷产品": {"mch_id": "302208100000044365"}},
            {"商户IP非白名单": {"mch_id": "302208100000044470"}},
            {"商户不存在": {"mch_id": "302207190000043502"}},
    ))
    def business_sign_verify_mch_state(self, mch_id):
        return list(mch_id.values())[0]


class BusinessIsignCancel:
    s = Strategy()

    @case(tags=['业务逻辑测试', '商户状态校验'])
    @parametrize(mch_id=(
            {"异常状态商户号": {"mch_id": "302208100000044473"}},
            # {"商户未订购快捷产品": {"mch_id": "302208100000044365"}},
            {"商户IP非白名单": {"mch_id": "302208100000044470"}},
            {"商户不存在": {"mch_id": "302207190000043502"}},
            {"没有签约记录": {"mch_id": "302207190000043504", "user_id": "149463736175", 'agree_no': '2022090609009247'}},
    ))
    def business_sign_cancel_mch_state(self, mch_id):
        return list(mch_id.values())[0]
