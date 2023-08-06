from __future__ import annotations

import base64
import hashlib
import hmac
import json
import threading
from datetime import datetime
from typing import Callable

import requests as re

from gmi_utils import GmiException, call_repeatedly
from okx.types import OkxInfoType, OkxTickerInfo


class OkxClient:
    def __init__(self, api_key: str, secret_key: str, passphrase: str, fee: float = 0.001) -> None:
        assert api_key is not None, "API_KEY can't be None"
        assert secret_key is not None, "SECRET_KEY can't be None"
        assert passphrase is not None, "PASSPHRASE can't be None"

        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__passphrase = passphrase
        self.fee = fee

        self.__data: dict[OkxInfoType, any] = {}
        self.__info_convars: dict[OkxInfoType, threading.Condition] = {}
        self.__info_locks: dict[OkxInfoType, threading.Lock] = {}
        self.__info_updaters: dict[OkxInfoType, Callable[[], None]] = {}
        self.__stop_updating_info: dict[OkxInfoType, Callable[[], None]] = {}

        self.__add_info_updater(OkxInfoType.BALANCE, self.__update_balance, 10 / 2)
        self.__add_info_updater(OkxInfoType.TICKERS, self.__update_tickers, 20 / 2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __auth_headers(self, method: str, *, request_path: str = '', body: str = '') -> dict[str, str]:
        timestamp = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        signature_raw = timestamp + method + request_path + body
        signature = hmac.new(self.__secret_key.encode('utf-8'), signature_raw.encode('utf-8'), hashlib.sha256).digest()
        auth_headers = {
            'OK-ACCESS-KEY': self.__api_key,
            'OK-ACCESS-SIGN': base64.b64encode(signature).decode('utf-8'),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.__passphrase,
        }
        return auth_headers

    def __add_info_updater(self, info_type: OkxInfoType, info_updater: Callable[[], None], rps: float) -> None:
        info_lock = threading.Lock()
        info_convar = threading.Condition()

        def info_updater_internal(lock: threading.Lock, convar: threading.Condition, updater: Callable[[], None]):
            with lock:
                updater()
                with convar:
                    convar.notify_all()

        info_updater_internal(info_lock, info_convar, info_updater)

        self.__info_locks[info_type] = info_lock
        self.__info_convars[info_type] = info_convar
        self.__stop_updating_info[info_type] = call_repeatedly(1 / rps,
                                                               info_updater_internal,
                                                               info_lock,
                                                               info_convar,
                                                               info_updater)

    def close(self):
        for stop_updating_info_func in self.__stop_updating_info.values():
            stop_updating_info_func()

    def __get(self, path: str, params=None, **kwargs):
        request_path = path
        if params is not None and len(params) > 0:
            first_param = True
            for param_name in params:
                request_path += f"{'?' if first_param else '&'}{param_name}={str(params[param_name])}"
                first_param = False
        headers = kwargs.pop('headers', {})
        kwargs.update(headers=self.__auth_headers('GET', request_path=request_path) | headers)
        resp = re.get('https://www.okx.com' + request_path, **kwargs).json()
        if 'code' not in resp:
            raise GmiException("Got response without 'code' field")
        elif resp['code'] != '0':
            raise GmiException(f"OKX returned error code {resp['code']}")
        elif 'data' not in resp:
            raise GmiException("Got response without 'data' field")
        return resp['data']

    def __post(self, path: str, body: dict, **kwargs):
        headers = kwargs.pop('headers', {})
        body_json = json.dumps(body)
        headers = self.__auth_headers('POST', request_path=path, body=body_json) | headers
        headers |= {'Content-Type': 'application/json'}
        kwargs.update(headers=headers)
        resp = re.post('https://www.okx.com' + path, data=body_json, **kwargs).json()
        if 'code' not in resp:
            raise GmiException("Got response without 'code' field")
        elif resp['code'] != '0':
            raise GmiException(f"OKX returned error code {resp['code']}")
        elif 'data' not in resp:
            raise GmiException("Got response without 'data' field")
        return resp['data']

    def invalidate_info(self, info_to_invalidate: list[OkxInfoType]) -> None:
        """Waits until all invalidated info is updated"""

        def waiter(info_type: OkxInfoType):
            convar = self.__info_convars[info_type]
            with convar:
                convar.wait()

        waiters = []
        for cur_info_type in info_to_invalidate:
            waiter_thread = threading.Thread(target=waiter, args=[cur_info_type])
            waiter_thread.start()
            waiters.append(waiter_thread)

        for waiter in waiters:
            waiter.join()

    def __get_data(self, info_type: OkxInfoType):
        with self.__info_locks[info_type]:
            if info_type not in self.__data:
                self.invalidate_info([info_type])
            return self.__data[info_type]

    def __update_balance(self):
        data = self.__get('/api/v5/account/balance')[0]

        balance_data: dict[str, float] = {}
        for details in data['details']:
            balance_data[details['ccy']] = float(details['availBal'])
        self.__data[OkxInfoType.BALANCE] = balance_data

    def get_balance(self, asset: str) -> float:
        return self.__get_data(OkxInfoType.BALANCE).get(asset, 0.)

    def __update_tickers(self):
        data = self.__get('/api/v5/market/tickers?instType=SPOT')

        tickers_data: dict[str, OkxTickerInfo] = {}
        for ticker in data:
            try:
                tickers_data[ticker['instId']] = OkxTickerInfo(askPrice=float(ticker['askPx']),
                                                               askSize=float(ticker['askSz']),
                                                               bidPrice=float(ticker['bidPx']),
                                                               bidSize=float(ticker['bidSz']))
            except ValueError:  # could not convert string to float
                pass  # that means there are no orders, so we just ignore ticker

        self.__data[OkxInfoType.TICKERS] = tickers_data

    def price_for(self, ask_amount: float, ask_asset: str, offer_asset: str) -> float:
        """How much {offer_asset} do I have to pay for {ask_amount}{ask_asset}?"""

        price: float
        tickers_data: dict[str, OkxTickerInfo] = self.__get_data(OkxInfoType.TICKERS)
        if (ticker := f'{offer_asset}-{ask_asset}') in tickers_data:
            ticker_info = tickers_data[ticker]
            price = (1. / ticker_info.bidPrice) * ask_amount
        elif (ticker := f'{ask_asset}-{offer_asset}') in tickers_data:
            ticker_info = tickers_data[ticker]
            price = ticker_info.askPrice * ask_amount
        else:
            raise GmiException(f"Can not find ticker for assets {ask_asset}/{offer_asset}")
        return price / (1. - self.fee)

    def amount_for(self, offer_amount: float, offer_asset: str, ask_asset: str) -> float:
        """How much {ask_asset} would I get for selling {offer_amount}{offer_asset}?"""

        amount: float
        tickers_data = self.__get_data(OkxInfoType.TICKERS)
        if (ticker := f'{offer_asset}-{ask_asset}') in tickers_data:
            ticker_info = tickers_data[ticker]
            amount = ticker_info.bidPrice * offer_amount
        elif (ticker := f'{ask_asset}-{offer_asset}') in tickers_data:
            ticker_info = tickers_data[ticker]
            amount = (1. / ticker_info.askPrice) * offer_amount
        else:
            raise GmiException(f"Can not find ticker for assets {offer_asset}/{ask_asset}")
        return amount * (1. - self.fee)

    def get_order_info(self, inst_id: str, order_id: str = None, client_order_id: str = None) -> any:
        """Returns order info: https://www.okx.com/docs-v5/en/#rest-api-trade-get-order-details"""

        if order_id is None and client_order_id is None:
            raise GmiException("Either order_id or client_order_id must be set to get order info")
        return self.__get('/api/v5/trade/order', params={
            'instId': inst_id,
            'ordId': order_id,
            'clOrdId': client_order_id,
        })

    def place_market_order(self, offer_amount: float, offer_asset: str, ask_asset: str) -> str:
        """Places market order and returns its id"""

        tickers_data = self.__get_data(OkxInfoType.TICKERS)
        if (ticker := f'{offer_asset}-{ask_asset}') in tickers_data:
            inst_id = ticker
            side = 'sell'
        elif (ticker := f'{ask_asset}-{offer_asset}') in tickers_data:
            inst_id = ticker
            side = 'buy'
        else:
            raise GmiException(f"Can not find ticker for assets {offer_asset}/{ask_asset}")

        data = self.__post('/api/v5/trade/order', body={
            'instId': inst_id,
            'tdMode': 'cash',
            'side': side,
            'ordType': 'market',
            'sz': str(offer_amount)
        })
        return data[0]['ordId']

    def complete_market_order(self, offer_amount: float, offer_asset: str, ask_asset: str) -> float:
        """Places market order and returns amount that was received (after fees)"""

        tickers_data = self.__get_data(OkxInfoType.TICKERS)
        if (ticker := f'{offer_asset}-{ask_asset}') in tickers_data:
            inst_id = ticker
        elif (ticker := f'{ask_asset}-{offer_asset}') in tickers_data:
            inst_id = ticker
        else:
            raise GmiException(f"Can not find ticker for assets {offer_asset}/{ask_asset}")

        order_id = self.place_market_order(offer_amount, offer_asset, ask_asset)

        order_completed = False
        order_info = {}
        while not order_completed:
            order_info = self.get_order_info(inst_id, order_id)[0]
            order_completed = (float(order_info['fillSz']) / float(order_info['sz'])) >= 0.999

        if order_info['side'] == 'sell':
            return (float(order_info['fillSz']) * float(order_info['fillPx'])) + float(order_info['fee'])
        else:
            return float(order_info['fillSz']) + float(order_info['fee'])

