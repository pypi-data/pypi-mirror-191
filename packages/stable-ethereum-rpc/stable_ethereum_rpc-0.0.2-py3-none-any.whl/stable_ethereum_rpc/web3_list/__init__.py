from typing import List, Dict

from stable_ethereum_rpc.web3_entity import SimpleWeb3Entity, Web3Entity
from stable_ethereum_rpc.web3_measure import Web3Measure


class BaseWeb3List:
    def __init__(self, chain_id: int, web3_list: List[SimpleWeb3Entity or str], **kwargs):
        self.chain_id = chain_id
        self._list: Dict[str, Web3Entity] = {}
        max_timestamp = kwargs.get("max_timestamp")
        self._measure = Web3Measure(chain_id, max_timestamp)
        for web3_item in web3_list:
            if isinstance(web3_item, str):
                self.add_web3(SimpleWeb3Entity(web3_item, "http"))
            else:
                self.add_web3(web3_item)

    def size(self):
        web3_keys = list(self._list.keys())
        _len = len(web3_keys)
        return _len

    def measure_all(self, **kwargs):
        web3_callback_func = kwargs.get("func")
        web3_keys = list(self._list.keys())
        _result = {}
        for web_key in web3_keys:
            temp_measure = self._measure.measure(self._list[web_key])
            web3_item = self._list[web_key]
            if callable(web3_callback_func):
                web3_callback_func(web3_item, temp_measure)
                _result[web_key] = {"measure": temp_measure, "item": web3_item}
        return _result

    def add_web3(self, web3_item: SimpleWeb3Entity, upsert=False) -> bool:
        provider_url = web3_item.provider_url
        rpc_type = web3_item.rpc_type
        is_exists = provider_url in self._list
        if upsert or (not is_exists):
            _temp = Web3Entity(provider_url, rpc_type, self.chain_id)
            self._list[provider_url] = _temp
            return True
        else:
            current_entity = self._list[provider_url]
            current_rpc_type = current_entity.rpc_type
            if current_rpc_type == rpc_type:
                return False
            else:
                _temp = Web3Entity(provider_url, rpc_type, self.chain_id)
                self._list[provider_url] = _temp
                return True

    def remove_web3(self, provider_url: str):
        if provider_url in self._list:
            del self._list[provider_url]
            return True
        return False
