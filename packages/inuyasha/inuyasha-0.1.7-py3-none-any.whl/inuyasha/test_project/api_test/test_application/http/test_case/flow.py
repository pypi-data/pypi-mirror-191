from pytest_cases import parametrize_with_cases

from lianlianpay_api.common_business.sms_code import get_sms_code
from lianlianpay_api.open_api.http.hook import ModifyProductOrder
from lianlianpay_api.open_api.http.template.interface import SignInterface
from lianlianpay_api.open_api.http.test_data.flow_data import FlowSignApplyVerify
from lianlianpay_api.open_api.http.test_data.flow_data import FlowSignApplyCancel
from lianlianpay_api.open_api.http.test_data.flow_data import FlowSignQuery
from utils.request_utils.requests_config import Config


class TestSignFlow:
    Config.is_cover_header = True
    i = SignInterface()

    @parametrize_with_cases('param', cases=FlowSignApplyVerify, prefix='main_', has_tag=['流程测试'])  # 主流程
    def test_isign_apply_verify(self, param):
        """
        签约申请验证流程
        """
        apply_response = self.i.isign_apply(param)
        token = apply_response.json()['token']
        verify_code = get_sms_code(phoneNo=param['bind_phone'])
        param['token'] = token
        param['verify_code'] = verify_code
        verify_response = self.i.isign_verify(param)
        return verify_response

    @parametrize_with_cases('param', cases=FlowSignApplyVerify, prefix='business_', has_tag=['流程测试', '逻辑测试'])  #
    def test_flow_isign_apply_verify_hook(self, param):
        """
        签约申请验证流程
        """
        ModifyProductOrder.modify_product_order_state(param['mch_id'], 'NORMAL')
        apply_response = self.i.isign_apply(param)
        token = apply_response.json()['token']
        verify_code = get_sms_code(phoneNo=param['bind_phone'])
        if 'token' not in param.keys():
            param['token'] = token
        if 'verify_code' not in param.keys():  # 如果有验证码，则不再获取验证码
            param['verify_code'] = verify_code
        if 'modify_product_state' in param.keys():  # 商户未订购快捷产品
            ModifyProductOrder.modify_product_order_state(param['mch_id'])
        verify_response = self.i.isign_verify(param)
        ModifyProductOrder.modify_product_order_state(param['mch_id'], 'NORMAL')
        return verify_response

    @parametrize_with_cases('param', cases=FlowSignApplyCancel, prefix='main_', has_tag=['流程测试'])
    def test_flow_isign_apply_verify_cancel(self, param):
        """
        签约解绑流程
        """
        verify_response = self.test_isign_apply_verify(param)
        param['agree_no'] = verify_response.json()['agree_no']
        cancel_response = self.i.isign_cancel(param)
        return cancel_response

    @parametrize_with_cases('param', cases=FlowSignQuery, prefix='main_', has_tag=['流程测试'])  # 主流程
    def test_isign_query(self, param):
        """
        签约申请验证流程
        """
        query_response = self.i.isign_query(param)
        return query_response
