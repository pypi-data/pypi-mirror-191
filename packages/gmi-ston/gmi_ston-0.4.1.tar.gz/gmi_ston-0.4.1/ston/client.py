from __future__ import annotations

import json
import math
import threading

import requests as re

from gmi_utils import GmiException, call_repeatedly


class StonClient:
    __instance = None

    def __init__(self) -> None:
        self.request_id: int = 0
        self.assets = {}
        self.addresses = {}
        self.pools = {}

        self.data_update_lock = threading.Lock()
        self.__update_data()
        self.stop_updating_data = call_repeatedly(5., self.__update_data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_updating_data()

    @classmethod
    def get_instance(cls) -> StonClient:
        if not cls.__instance:
            cls.__instance = StonClient()
        return cls.__instance

    def __get_request_id(self) -> int:
        self.request_id += 1
        return self.request_id

    def ston_request(self, method: str, params: json) -> json:
        return re.post("https://app.ston.fi/rpc", json={
            "id": self.__get_request_id(),
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }).json()

    def __update_data(self) -> None:
        self.data_update_lock.acquire()

        pool_list = self.ston_request("pool.list", {})
        self.pools = {}
        for pool in pool_list['result']['pools']:
            if pool['token0_address'] not in self.assets or pool['token1_address'] not in self.assets:
                assets = self.ston_request("asset.list", {"prev_version": None})
                self.assets = {}
                for asset in assets['result']['assets']:
                    self.assets[asset['contract_address']] = asset
                # Old WTON address
                self.assets['EQDKzORo0q1obYK1EQ32S-qOl5NIIKfGm8qDdc6dDj-BYOjX'] = \
                    self.assets['EQDQoc5M3Bh8eWFephi9bClhevelbZZvWhkqdo80XuY_0qXv']

                self.addresses = {}
                for asset in assets['result']['assets']:
                    self.addresses[asset['symbol']] = asset['contract_address']

            if pool['token0_address'] in self.assets and pool['token1_address'] in self.assets:
                pool['token0_symbol'] = self.assets[pool['token0_address']]['symbol']
                pool['token1_symbol'] = self.assets[pool['token1_address']]['symbol']
                self.pools[(pool['token0_address'], pool['token1_address'])] = pool
                self.pools[(pool['token1_address'], pool['token0_address'])] = pool

        self.data_update_lock.release()

    def get_symbol(self, token_address: str) -> str:
        return self.assets[token_address]['symbol']

    def get_address(self, symbol: str) -> str:
        return self.addresses[symbol]

    def from_decimals(self, amount: int, token_address: str) -> float:
        return amount / (10 ** self.assets[token_address]['decimals'])

    def to_decimals(self, amount: float, token_address: str) -> int:
        return amount * (10 ** self.assets[token_address]['decimals'])

    def get_token_symbol(self, token_address: str):
        return self.assets[token_address]['symbol']

    def dex_simulate_swap(self, ask_address: str, offer_address: str, offer_units: int, slippage_tolerance: float) \
            -> int:
        res = self.ston_request("dex.simulate_swap", {
            "ask_address": ask_address,
            "offer_address": offer_address,
            "offer_units": str(offer_units),
            "slippage_tolerance": str(slippage_tolerance),
        })
        if 'result' in res:
            return int(res['result']['min_ask_units'])
        else:
            raise GmiException(res['error']['message'])

    def get_asset_balance(self, wallet_address: str, token_address: str) -> int:
        res = self.ston_request('asset.balance_list', {'wallet_address': wallet_address})
        if 'result' in res:
            for asset_info in res['result']['assets']:
                if asset_info['contract_address'] == token_address:
                    return int(asset_info['balance'])
            raise GmiException("Unknown asset")
        else:
            raise GmiException(res['error']['message'])

    @staticmethod
    def get_max_pool_fee(pool) -> float:
        return (float(pool['lp_fee']) + float(pool['ref_fee'])) / 10000.

    def simulate_swap(self, ask_address: str, offer_address: str, offer_units: int, slippage_tolerance: float) -> int:
        if offer_units < 1:
            return 0
        if (ask_address, offer_address) not in self.pools:
            raise GmiException(f"Unknown asset pair {ask_address} / {offer_address}")
        pool = self.pools[(ask_address, offer_address)]
        old_ask_units = int(pool['reserve0'] if ask_address == pool['token0_address'] else pool['reserve1'])
        old_offer_units = int(pool['reserve0'] if offer_address == pool['token0_address'] else pool['reserve1'])
        constant_product = old_ask_units * old_offer_units
        new_offer_units = old_offer_units + offer_units
        new_ask_units = constant_product / new_offer_units
        ask_units = old_ask_units - new_ask_units
        return int(ask_units * (1. - slippage_tolerance) * (1. - self.get_max_pool_fee(pool)))

    def find_best_3_segment_path(self, initial_token_address: str, initial_balance: int, slippage_tolerance: float) \
            -> tuple[list[str], int]:
        analyzed_paths = 0
        total_paths = len(self.assets) * len(self.assets)
        # print(f"Analyzing paths... Found {total_paths}")
        best_path = ([], 0)
        for token1_address in self.assets:
            if token1_address != initial_token_address:
                for token2_address in self.assets:
                    if token2_address != token1_address and token2_address != initial_token_address:  # TON address
                        res = None
                        try:
                            cur_balance = initial_balance
                            # print(f"{self.from_decimals(cur_balance, initial_token_address)} "
                            #       f"{self.assets[initial_token_address]['symbol']} -> ", end="")

                            cur_balance = self.simulate_swap(token1_address, initial_token_address,
                                                             cur_balance, slippage_tolerance)
                            # print(f"{self.from_decimals(int(cur_balance), token1_address)} "
                            #       f"{self.assets[token1_address]['symbol']} -> ", end="")

                            cur_balance = self.simulate_swap(token2_address, token1_address,
                                                             cur_balance, slippage_tolerance)
                            # print(f"{self.from_decimals(int(cur_balance), token2_address)} "
                            #       f"{self.assets[token2_address]['symbol']} -> ", end="")

                            cur_balance = self.simulate_swap(initial_token_address, token2_address,
                                                             cur_balance, slippage_tolerance)
                            # print(f"{self.from_decimals(cur_balance, initial_token_address)} "
                            #       f"{self.assets[initial_token_address]['symbol']}")

                            if cur_balance > best_path[1] or len(best_path[0]) == 0:
                                best_path = ([initial_token_address, token1_address, token2_address], cur_balance)

                        except Exception as e:
                            print(e)
                            pass
                    analyzed_paths += 1
                    # print(f"Finished {analyzed_paths}/{total_paths} ({analyzed_paths * 100 / total_paths}%)")
            else:
                analyzed_paths += len(self.assets)
                # print(f"Finished {analyzed_paths}/{total_paths} ({analyzed_paths * 100 / total_paths}%)")
        return best_path

    def __find_best_path(self, initial_token_address: str, cur_balance: int, slippage_tolerance: float,
                         cur_path: list[str], unused_assets: list[str]) -> tuple[list[str], int]:
        best_path = ([], -math.inf)
        unused_assets_copy = unused_assets.copy()
        for asset in unused_assets:
            if asset != '#END':
                unused_assets_copy.remove(asset)
                cur_path.append(asset)

                try:
                    next_balance = self.simulate_swap(asset, cur_path[-2], cur_balance, slippage_tolerance)
                    cur_best_path = self.__find_best_path(initial_token_address, next_balance, slippage_tolerance,
                                                          cur_path, unused_assets_copy)
                    if cur_best_path[1] > best_path[1]:
                        best_path = cur_best_path
                except Exception as e:
                    pass

                cur_path.pop()
                unused_assets_copy.append(asset)
            else:
                try:
                    result_balance = self.simulate_swap(initial_token_address, cur_path[-1], cur_balance,
                                                        slippage_tolerance)
                    result_balance -= self.to_decimals(self.get_swap_path_commission(cur_path),
                                                       'EQDQoc5M3Bh8eWFephi9bClhevelbZZvWhkqdo80XuY_0qXv')  # WTON
                    if result_balance > best_path[1]:
                        best_path = (cur_path.copy(), result_balance)
                except Exception as e:
                    pass
        return best_path

    def find_best_path(self, initial_token_address: str, initial_balance: int, slippage_tolerance: float) \
            -> tuple[list[str], int]:
        assets = list(str(x) for x in self.assets.keys())
        assets.remove(initial_token_address)

        # TODO: add special logic for TON<->WTON swaps
        if initial_token_address == 'EQDQoc5M3Bh8eWFephi9bClhevelbZZvWhkqdo80XuY_0qXv':  # WTON
            assets.remove('EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c')  # TON
        elif initial_token_address == 'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c':  # TON
            assets.remove('EQDQoc5M3Bh8eWFephi9bClhevelbZZvWhkqdo80XuY_0qXv')  # WTON

        assets.remove('EQDKzORo0q1obYK1EQ32S-qOl5NIIKfGm8qDdc6dDj-BYOjX')  # legacy WTON address
        assets.append('#END')
        cur_path = [initial_token_address]
        return self.__find_best_path(initial_token_address, initial_balance, slippage_tolerance, cur_path, assets)

    def calculate_balance_after_path(self, path: list[str], start_balance: int, slippage_tolerance: float) -> int:
        balance = start_balance
        for offer_token_idx in range(len(path) - 1):
            balance = self.simulate_swap(path[offer_token_idx + 1], path[offer_token_idx], balance, slippage_tolerance)
        balance = self.simulate_swap(path[0], path[-1], balance, slippage_tolerance)
        balance -= self.to_decimals(self.get_swap_path_commission(path),
                                    'EQDQoc5M3Bh8eWFephi9bClhevelbZZvWhkqdo80XuY_0qXv')  # WTON
        return balance

    def calculate_path_profit(self, path: list[str], start_balance: int, slippage_tolerance: float) -> int:
        return self.calculate_balance_after_path(path, start_balance, slippage_tolerance) - start_balance

    def get_max_exploitable_value(self, path: list[str], max_balance: int, slippage_tolerance: float) -> (int, int):
        lb = 0
        rb = max_balance
        while rb - lb > 10:
            t = (rb - lb) // 3
            m1 = lb + t
            m2 = rb - t
            if self.calculate_path_profit(path, m1, slippage_tolerance) < \
                    self.calculate_path_profit(path, m2, slippage_tolerance):
                lb = m1
            else:
                rb = m2
        return lb, self.calculate_balance_after_path(path, lb, slippage_tolerance)

    def get_swap_commission(self, token0_address: str, token1_address: str) -> float:
        if self.get_address('TON') in [token0_address, token1_address]:
            return 0.09  # TON
        else:
            return 0.13  # TON

    def get_swap_path_commission(self, path: list[str]) -> float:
        total_commission = 0.
        for offer_token_idx in range(len(path) - 1):
            total_commission += self.get_swap_commission(path[offer_token_idx + 1], path[offer_token_idx])
        total_commission += self.get_swap_commission(path[0], path[-1])
        return total_commission

    def swap(self,
             wallet_mnemonics: str,
             bid_amount: float,
             bid_token_address: str,
             min_ask_amount: float,
             ask_token_address: str) -> bool:
        from ston.__swapper import _swap
        return _swap(self, wallet_mnemonics, bid_amount, bid_token_address, min_ask_amount, ask_token_address)
