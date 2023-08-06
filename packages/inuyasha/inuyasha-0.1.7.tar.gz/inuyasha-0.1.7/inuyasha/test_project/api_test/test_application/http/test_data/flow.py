from faker import Faker
from pytest_cases import case, parametrize

fake = Faker("zh-CN")


class FlowSignApplyVerify:

    @case(tags=['流程测试', '主流程'])
    @parametrize(data=(
            {"借记卡正常签约": {"card_no": f'62170052952066' + str(fake.random_number(5))}},
            {"信用卡正常签约": {"card_no": f'62257613808' + str(fake.random_number(5))}},
            # {"用户已解约再次签约": {"user_id": "661881918869", "card_no": "6222625295206805180", "id_no": "510500195204118570", "acct_name": "陈桂芳", "bind_phone": "15017792705"}},
            # {"同一个用户更换四要素签约": {"user_id": "417381486785"}},
    ))
    def main_sign_apply_verify(self, data):
        template = {
            "mch_id": '302207190000043504',  # 商户号
            "user_id": str(fake.random_number(12)),  # 用户唯一编号
            "bind_phone": fake.phone_number(),  # 绑定手机号
        }
        template.update(list(data.values())[0])
        return template

    @case(tags=['流程测试', '逻辑测试'])
    @parametrize(data=(
            {"商户未订购快捷产品": {"mch_id": "302208100000044359", "modify_product_state": True}},
            {"仅短信验证码错误": {"verify_code": "711969"}},
            {"仅Token错误-其他商户的token": {"token": "5F6C3B141AE6C35288DA830A7F8D6271"}},
            {"仅Token错误-该商户的token": {"token": "92804AA35A09DCDC27B1FC6B263E4342"}},
            {"短信验证码错误-Token错误": {"token": "78D27679849E4785A6BF50008472374C", "verify_code": "711969"}},
    ))
    def business_sign_apply_verify(self, data):
        template = {
            "mch_id": "302112300000007010",
            "sub_mchid": "602202200000014203",
            "user_id": str(fake.random_number(12)),  # 用户唯一编号
            "bind_phone": fake.phone_number(),  # 绑定手机号
        }
        template.update(list(data.values())[0])
        return template


class FlowSignApplyCancel:

    @case(tags=['流程测试', '主流程'])
    @parametrize(data=(
            {"借记卡正常解约": {"card_no": f'62170052952066' + str(fake.random_number(5))}},
            # {"信用卡正常解约": {"card_no": f'62257613808' + str(fake.random_number(5))}},
            # {"用户已解约再次签约解约": {"user_id": "661881918869", "card_no": "6222625295206805180", "id_no": "510500195204118570", "acct_name": "陈桂芳", "bind_phone": "15017792705"}},
            # {"同一个用户更换四要素签约解约": {"user_id": "417381486785"}},
    ))
    def main_sign_apply_verify(self, data):
        template = {
            "mch_id": '302112300000007010',  # 商户号
            "user_id": str(fake.random_number(12)),  # 用户唯一编号
            "bind_phone": fake.phone_number(),  # 绑定手机号
        }
        template.update(list(data.values())[0])
        return template


class FlowSignQuery:

    @case(tags=['流程测试', '主流程'])
    @parametrize(data=(
            {"借记卡签约查询": {"card_no": f'62170052952066' + str(fake.random_number(5))}},
            {"信用卡签约查询": {"card_no": f'62257613808' + str(fake.random_number(5))}},
    ))
    def main_sign_apply_verify(self, data):
        template = {
            "mch_id": '302207190000043504',  # 商户号
            "user_id": str(fake.random_number(12)),  # 用户唯一编号
            "bind_phone": fake.phone_number(),  # 绑定手机号
        }
        template.update(list(data.values())[0])
        return template
