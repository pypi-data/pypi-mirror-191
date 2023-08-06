from pytest_cases import parametrize_with_cases

from lianlianpay_api.open_api.http.template.interface import SignInterface
from lianlianpay_api.open_api.http.test_data.interface_data import InterfaceIsignCardbin
from lianlianpay_api.open_api.http.test_data.interface_data import InterfaceIsignQuery
from lianlianpay_api.open_api.http.test_data.interface_data import InterfaceIsignApply
from lianlianpay_api.open_api.http.test_data.interface_data import InterfaceIsignVerify
from lianlianpay_api.open_api.http.test_data.interface_data import InterfaceIsignCancel
from utils.request_utils.requests_config import Config


class TestSignInterface:
    i = SignInterface()
    Config.is_cover_header = False

    @parametrize_with_cases('param', cases=InterfaceIsignCardbin, prefix="interface_", has_tag=['单接口测试'])  # 单接口测试
    def test_isign_cardbin(self, param):
        return self.i.isign_cardbin(param)

    @parametrize_with_cases('param', cases=InterfaceIsignQuery, prefix="interface_", has_tag=['单接口测试'])  # 单接口测试
    def test_isign_query(self, param):
        return self.i.isign_query(param)

    @parametrize_with_cases('param', cases=InterfaceIsignApply, prefix="interface_", has_tag=['单接口测试'])  # 单接口测试
    def test_isign_apply(self, param):
        return self.i.isign_apply(param)

    @parametrize_with_cases('param', cases=InterfaceIsignVerify, prefix="interface_", has_tag=['单接口测试'])  # 单接口测试
    def test_isign_verify(self, param):
        return self.i.isign_verify(param)

    @parametrize_with_cases('param', cases=InterfaceIsignCancel, prefix="interface_", has_tag=['单接口测试'])  # 单接口测试
    def test_isign_cancel(self, param):
        return self.i.isign_cancel(param)


if __name__ == '__main__':
    from faker import Faker
    import emoji

    fake = Faker("zh-CN")
    emoji.emojize(':thumbs_up:')
    str(fake.random_number(32))
    data = {
        'card_no': f'6222625295206' + str(fake.random_number(6)),
        'id_no': fake.ssn(),
        'acct_name': fake.name(),
        'bind_phone': fake.phone_number(),
        "user_id": str(fake.random_number(12)),
    }
    # apply_response = isign_apply('RSA', 'RSA', 'Header', **data)
    # query_response = isign_query('RSA', 'RSA', 'Header')
    # carbin_response = isign_cardbin('RSA', 'RSA', 'Header')
