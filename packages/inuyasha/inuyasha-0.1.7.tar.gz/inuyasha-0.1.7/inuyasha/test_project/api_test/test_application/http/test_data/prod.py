from faker import Faker
from pytest_cases import case, parametrize

fake = Faker("zh-CN")


class FlowSignApplyVerify:

    @case(tags=['流程测试', '主流程'])
    @parametrize(data=(
            {"用户正常签约": {"mch_id": '302207190000043504'}},
    ))
    def main_sign_apply_verify(self, data):
        template = {
            "mch_id": '302207190000043504',  # 商户号
            "user_id": str(fake.random_number(12)),  # 用户唯一编号
            "bind_phone": fake.phone_number(),  # 绑定手机号
        }
        template.update(list(data.values())[0])
        return template


class FlowSignApplyCancel:

    @case(tags=['流程测试', '主流程'])
    @parametrize(data=(
            {"用户正常解约": {"mch_id": '302207190000043504'}},
    ))
    def main_sign_apply_verify(self, data):
        template = {
            "mch_id": '302207190000043504',  # 商户号
            "user_id": str(fake.random_number(12)),  # 用户唯一编号
            "bind_phone": fake.phone_number(),  # 绑定手机号
        }
        template.update(list(data.values())[0])
        return template
