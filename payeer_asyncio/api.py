from .exceptions import PayeerAPIException
from .utils.account import validate_account
from typing import (
    Dict
)
import httpx
import copy




class PayeerAsyncIO:
    """Payeer API Client"""

    def __init__(self, account: str, apiId: str, apiPass: str):
        """
        :param account: Your account number in the Payeer. Example: P1000000
        :param apiId: The API user ID; given out when adding the API
        :param apiPass: The API user's secret key
        """
        self.account = account
        self.apiId = apiId
        self.apiPass = apiPass
        self.api_url = 'https://payeer.com/ajax/api/api.php'
        self.auth_data = {
            'account': self.account,
            'apiId': self.apiId,
            'apiPass': self.apiPass
            }


    async def request(self, **kwargs) -> Dict:
        """The main request method for Payeer API"""

        data = copy.deepcopy(self.auth_data)

        if kwargs:
            data.update(kwargs)

        async with httpx.AsyncClient() as client:
            http_resp = await client.post(self.api_url, data=data)
            resp_json = http_resp.json()

            error = resp_json.get('errors')
            if error:
                raise PayeerAPIException(error)
            else:
                return resp_json


    async def get_balance(self):
        """
        Balance Check
        Obtain wallet balance.
        """
        return (await self.request(action='balance'))['balance']


    async def check_user(self, user):
        """
        Checking Existence of Account
        :param user: user’s account number in the format P1000000
        :return: True if exists
        """
        try:
            await self.request(action='checkUser', user=user)
        except PayeerAPIException:
            return False
        return True


    async def get_exchange_rate(self, output='N'):
        """
        Automatic Conversion Rates
        :param output: select currencies for conversion rates (N - get deposit rates Y - get withdrawal rates)
        :return: dict
        """
        return (await self.request(action='getExchangeRate', output=output))['rate']


    async def get_pay_systems(self):
        """
        Getting Available Payment Systems
        :return: dict
        """
        return (await self.request(action='getPaySystems'))['list']


    async def get_history_info(self, history_id):
        """
        Getting Information about a Transaction
        :param history_id: transaction ID
        :return: dict
        """
        return (await self.request(action='historyInfo', historyId=history_id))['info']


    async def shop_order_info(self, shop_id, order_id):
        """
        Information on a Store Transaction
        :param shop_id: merchant ID (m_shop)
        :param order_id: transaction ID in your accounting system (m_orderid)
        :return: dict
        """
        return await self.request(action='shopOrderInfo', shopId=shop_id, orderId=order_id)


    async def transfer(self, sum, to, cur_in='USD', cur_out='USD',
                       comment=None, protect=None, protect_period=None, protect_code=None):
        """
        Transferring Funds
        :param sum: amount withdrawn (the amount deposited will be calculated automatically, factoring in all fees from the recipient)
        :param to: user’s Payeer account number or email address
        :param cur_in: currency with which the withdrawal will be performed	(USD, EUR, RUB)
        :param cur_out: deposit currency (USD, EUR, RUB)
        :param comment: comments on the transfer
        :param protect: activation of transaction protection, set Y to enable
        :param protect_period: protection period: 1–30 days
        :param protect_code: protection code
        :return: True if the payment is successful
        """
        await validate_account(to)
        data = {'action': 'transfer', 'sum': sum, 'to': to, 'curIn': cur_in, 'curOut': cur_out}
        if comment:
            data['comment'] = comment
        if protect:
            data['protect'] = protect
            if protect_period:
                data['protectPeriod'] = protect_period
            if protect_code:
                data['protectCode'] = protect_code

        return await self.request(**data)


    async def check_output(self, ps, ps_account, sum_in, cur_in='USD', cur_out='USD'):
        """
        Checking Possibility of Payout
        This method allows you to check the possibility of a payout without actually creating a payout
        (you can get the withdrawal/reception amount or check errors in parameters)
        :param ps: ID of selected payment system
        :param ps_account: recipient's account number in the selected payment system
        :param sum_in: amount withdrawn (the amount deposited will be calculated automatically, factoring in all fees from the recipient)
        :param cur_in: currency with which the withdrawal will be performed
        :param cur_out: deposit currency
        :return: True if the payment is successful
        """
        data = {'action': 'initOutput', 'ps': ps, 'param_ACCOUNT_NUMBER': ps_account,
                'sumIn': sum_in, 'curIn': cur_in, 'curOut': cur_out}
        try:
            await self.request(**data)
        except PayeerAPIException:
            return False
        return True


    async def output(self, ps, ps_account, sum_in, cur_in='USD', cur_out='USD'):
        """
        Payout
        :param ps: ID of selected payment system
        :param ps_account: recipient's account number in the selected payment system
        :param sum_in: amount withdrawn (the amount deposited will be calculated automatically, factoring in all fees from the recipient)
        :param cur_in: currency with which the withdrawal will be performed
        :param cur_out: deposit currency
        :return:
        """
        data = {'action': 'output', 'ps': ps, 'param_ACCOUNT_NUMBER': ps_account,
                'sumIn': sum_in, 'curIn': cur_in, 'curOut': cur_out}
        return await self.request(**data)


    async def history(self, **kwargs):
        """
        History of transactions
        :param sort: sorting by date (asc, desc)
        :param count: count of records (max 1000)
        :param from: begin of the period
        :param to: end of the period
        :param type: transaction type (incoming - incoming payments, outgoing - outgoing payments)
        :param append: id of the previous transaction
        :return:
        """
        kwargs['action'] = 'history'
        return (await self.request(**kwargs))['history']



