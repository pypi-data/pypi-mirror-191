from pytest_cases import case, parametrize

from utils.data_utils.single_interface.strategy import Strategy, StrategyConfig


class InterfaceIsignCardbin:
    s = Strategy()

    @case(tags='单接口测试')
    @parametrize(mch_id=s.gen_field_response('mch_id', StrategyConfig(length_config=18, null_provider=['字符串'])))
    def interface_sign_cardbin_mch_id(self, mch_id):
        return mch_id

    # @case(tags='单接口测试')
    # @parametrize(sub_mchid=s.gen_field_response('sub_mchid', StrategyConfig(length_config=18, null_provider=['字符串'])))
    # def interface_sign_cardbin_sub_mchid(self, sub_mchid):
    #     return sub_mchid

    @case(tags='单接口测试')
    @parametrize(user_id=s.gen_field_response('user_id', StrategyConfig(length_config=64, null_provider=['字符串'])))
    def interface_sign_cardbin_user_id(self, user_id):
        return user_id

    @case(tags='单接口测试')
    @parametrize(card_no=s.gen_field_response(
        'card_no', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_cardbin_card_no(self, card_no):
        return card_no


class InterfaceIsignQuery:
    s = Strategy()

    @case(tags='单接口测试')
    @parametrize(mch_id=s.gen_field_response('mch_id', StrategyConfig(length_config=18, null_provider=['字符串'])))
    def interface_sign_query_mch_id(self, mch_id):
        return mch_id

    # @case(tags='单接口测试')
    # @parametrize(sub_mchid=s.gen_field_response('sub_mchid', StrategyConfig(length_config=18, null_provider=['字符串'])))
    # def interface_sign_query_sub_mchid(self, sub_mchid):
    #     return sub_mchid

    @case(tags='单接口测试')
    @parametrize(user_id=s.gen_field_response('user_id', StrategyConfig(length_config=64, null_provider=['字符串'])))
    def interface_sign_query_user_id(self, user_id):
        return user_id


class InterfaceIsignApply:
    s = Strategy()

    @case(tags='单接口测试')
    @parametrize(mch_id=s.gen_field_response('mch_id', StrategyConfig(length_config=18, null_provider=['字符串'])))
    def interface_sign_apply_mch_id(self, mch_id):
        return mch_id

    # @case(tags='单接口测试')
    # @parametrize(sub_mchid=s.gen_field_response('sub_mchid', StrategyConfig(length_config=18, null_provider=['字符串'])))
    # def interface_sign_apply_sub_mchid(self, sub_mchid):
    #     return sub_mchid

    @case(tags='单接口测试')
    @parametrize(user_id=s.gen_field_response('user_id', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_apply_user_id(self, user_id):
        return user_id

    @case(tags='单接口测试')
    @parametrize(txn_seqno=s.gen_field_response('txn_seqno', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_apply_txn_seqno(self, txn_seqno):
        return txn_seqno

    @case(tags='单接口测试')
    @parametrize(txn_time=s.gen_field_response(
        'txn_time', StrategyConfig(length_config=14, null_provider=['字符串'])))
    def interface_sign_apply_txn_time(self, txn_time):
        return txn_time

    @case(tags='单接口测试')
    @parametrize(card_info=s.gen_field_response(
        'card_info', StrategyConfig(length_config=32, category_provider=['空'], null_provider=['字典'])))
    def interface_sign_apply_card_info(self, card_info):
        return card_info

    @case(tags='单接口测试')
    @parametrize(card_no=s.gen_field_response(
        'card_no', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_apply_card_no(self, card_no):
        return card_no

    @case(tags='单接口测试')
    @parametrize(id_type=s.gen_field_response(
        'id_type', StrategyConfig(length_config=6, category_config='字母', category_provider=['字母', '空'], null_provider=['字符串'], rule_provider='IDCARD')))
    def interface_sign_apply_id_type(self, id_type):
        return id_type

    @case(tags='单接口测试')
    @parametrize(id_no=s.gen_field_response(
        'id_no', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_apply_id_no(self, id_no):
        return id_no

    @case(tags='单接口测试')
    @parametrize(acct_name=s.gen_field_response(
        'acct_name', StrategyConfig(length_config=64, category_config='汉字', null_provider=['字符串'])))
    def interface_sign_apply_acct_name(self, acct_name):
        return acct_name

    @case(tags='单接口测试')
    @parametrize(bind_phone=s.gen_field_response(
        'bind_phone', StrategyConfig(length_config=11, null_provider=['字符串'])))
    def interface_sign_apply_bind_phone(self, bind_phone):
        return bind_phone


class InterfaceIsignVerify:
    s = Strategy()

    @case(tags='单接口测试')
    @parametrize(mch_id=s.gen_field_response('mch_id', StrategyConfig(length_config=18, null_provider=['字符串'])))
    def interface_sign_verify_mch_id(self, mch_id):
        return mch_id

    # @case(tags='单接口测试')
    # @parametrize(sub_mchid=s.gen_field_response('sub_mchid', StrategyConfig(length_config=18, null_provider=['字符串'])))
    # def interface_sign_verify_sub_mchid(self, sub_mchid):
    #     return sub_mchid

    @case(tags='单接口测试')
    @parametrize(user_id=s.gen_field_response('user_id', StrategyConfig(length_config=64, null_provider=['字符串'])))
    def interface_sign_verify_user_id(self, user_id):
        return user_id

    @case(tags='单接口测试')
    @parametrize(token=s.gen_field_response('token', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_verify_token(self, token):
        return token

    @case(tags='单接口测试')
    @parametrize(verify_code=s.gen_field_response('verify_code', StrategyConfig(length_config=6, null_provider=['字符串'])))
    def interface_sign_verify_verify_code(self, verify_code):
        return verify_code


class InterfaceIsignCancel:
    s = Strategy()

    @case(tags='单接口测试')
    @parametrize(mch_id=s.gen_field_response('mch_id', StrategyConfig(length_config=18, null_provider=['字符串'])))
    def interface_sign_verify_mch_id(self, mch_id):
        return mch_id

    # @case(tags='单接口测试')
    # @parametrize(sub_mchid=s.gen_field_response('sub_mchid', StrategyConfig(length_config=18, null_provider=['字符串'])))
    # def interface_sign_verify_sub_mchid(self, sub_mchid):
    #     return sub_mchid

    @case(tags='单接口测试')
    @parametrize(user_id=s.gen_field_response('user_id', StrategyConfig(length_config=64, null_provider=['字符串'])))
    def interface_sign_verify_user_id(self, user_id):
        return user_id

    @case(tags='单接口测试')
    @parametrize(card_info=s.gen_field_response(
        'card_info', StrategyConfig(length_config=32, category_provider=['空'], null_provider=['字典'])))
    def interface_sign_apply_card_info(self, card_info):
        return card_info

    @case(tags='单接口测试')
    @parametrize(agree_no=s.gen_field_response('agree_no', StrategyConfig(length_config=32, null_provider=['字符串'])))
    def interface_sign_verify_agree_no(self, agree_no):
        return agree_no
