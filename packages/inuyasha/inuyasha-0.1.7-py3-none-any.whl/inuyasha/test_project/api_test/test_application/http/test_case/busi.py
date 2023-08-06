from pytest_cases import parametrize_with_cases

from lianlianpay_api.open_api.http.template.interface import SignInterface
from lianlianpay_api.open_api.http.test_data.business_data import BusinessIsignCardbin
from lianlianpay_api.open_api.http.test_data.business_data import BusinessIsignQuery
from lianlianpay_api.open_api.http.test_data.business_data import BusinessIsignApply
from lianlianpay_api.open_api.http.test_data.business_data import BusinessIsignVerify
from lianlianpay_api.open_api.http.test_data.business_data import BusinessIsignCancel
from utils.request_utils.requests_config import Config


class TestSignInterface:
    i = SignInterface()
    Config.is_cover_header = True

    @parametrize_with_cases('param', cases=BusinessIsignCardbin, prefix="business_", has_tag=['业务逻辑测试'])  # 业务逻辑测试
    # @parametrize_with_cases('param', cases=BusinessIsignCardbin, prefix="business_", has_tag=['业务逻辑测试', '签约状态校验'])  # 业务逻辑测试
    def test_isign_cardbin(self, param):
        return self.i.isign_cardbin(param)

    @parametrize_with_cases('param', cases=BusinessIsignQuery, prefix="business_", has_tag=['业务逻辑测试'])  # 业务逻辑测试
    def test_isign_query(self, param):
        return self.i.isign_query(param)

    @parametrize_with_cases('param', cases=BusinessIsignApply, prefix="business_", has_tag=['业务逻辑测试'])  # 业务逻辑测试
    def test_isign_apply(self, param):
        return self.i.isign_apply(param)

    @parametrize_with_cases('param', cases=BusinessIsignVerify, prefix="business_", has_tag=['业务逻辑测试', '商户状态校验'])  # 业务逻辑测试
    def test_isign_verify(self, param):
        return self.i.isign_verify(param)

    @parametrize_with_cases('param', cases=BusinessIsignCancel, prefix="business_", has_tag=['业务逻辑测试'])  # 业务逻辑测试
    def test_isign_cancel(self, param):
        return self.i.isign_cancel(param)
