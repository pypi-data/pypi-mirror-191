from abc import ABC, abstractmethod
import asyncio
import aiohttp
from tvm_valuetypes import serialize_tvm_stack

from tonsdk.provider import ToncenterClient, prepare_address, address_state
from tonsdk.utils import TonCurrencyEnum, from_nano
from tonsdk.boc import Cell


class __AbstractTonClient(ABC):
    @abstractmethod
    def _run(self, to_run, *, single_query=True):
        self.provider = None
        raise NotImplemented

    def get_address_information(self, address: str,
                                currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        return self.get_addresses_information([address], currency_to_show)[0]

    def get_addresses_information(self, addresses,
                                  currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        if not addresses:
            return []

        tasks = []
        for address in addresses:
            address = prepare_address(address)
            tasks.append(self.provider.raw_get_account_state(address))

        results = self._run(tasks, single_query=False)

        for result in results:
            result["state"] = address_state(result)
            if "balance" in result:
                if int(result["balance"]) < 0:
                    result["balance"] = 0
                else:
                    result["balance"] = from_nano(
                        int(result["balance"]), currency_to_show)

        return results

    def seqno(self, addr: str):
        addr = prepare_address(addr)
        result = self._run(self.provider.raw_run_method(addr, "seqno", []))

        if 'stack' in result and ('@type' in result and result['@type'] == 'smc.runResult'):
            result['stack'] = serialize_tvm_stack(result['stack'])

        return result

    def send_boc(self, boc: Cell):
        return self._run(self.provider.raw_send_message(boc))

    def call2(self, address: str, method_name: str, stack_data: list[list[str]]):
        return self._run(self.provider.raw_run_method(address, method_name, stack_data))


class _TonCenterTonClient(__AbstractTonClient):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.provider = ToncenterClient(base_url="https://toncenter.com/api/v2/",
                                        api_key="97450c5a9512e87b3f4c5e8344a00311d67868cc94834c0ccd9e914db30a06b5")

    def _run(self, to_run, *, single_query=True):
        try:
            return self.loop.run_until_complete(
                self.__execute(to_run, single_query))

        # ToncenterWrongResult, asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError
        except Exception:
            raise

    async def __execute(self, to_run, single_query):
        timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(timeout=timeout) as self.session:
            if single_query:
                to_run = [to_run]

            tasks = []
            for task in to_run:
                tasks.append(task["func"](self.session, *task["args"], **task["kwargs"]))

            return await asyncio.gather(*tasks)


class TonClient:
    def __init__(self, address: str):
        self.__client = _TonCenterTonClient()
        self.address = address

    def seqno(self):
        return self.__client.seqno(self.address)

    def send_boc(self, boc: Cell):
        return self.__client.send_boc(boc)

    def call2(self, address: str, method_name: str, stack_data: list[list[str]]):
        return self.__client.call2(address, method_name, stack_data)
