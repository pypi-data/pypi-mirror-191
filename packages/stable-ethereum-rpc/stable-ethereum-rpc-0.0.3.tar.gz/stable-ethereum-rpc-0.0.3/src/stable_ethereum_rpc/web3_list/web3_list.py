from typing import List

from stable_ethereum_rpc.web3_entity import SimpleWeb3Entity, Web3Entity
from stable_ethereum_rpc.web3_list import BaseWeb3List


class Web3List(BaseWeb3List):
    def __init__(self, chain_id: int, web3_list: List[SimpleWeb3Entity or str], **kwargs):
        super().__init__(chain_id, web3_list, **kwargs)

    def get_sufficient_web3(self, **kwargs) -> Web3Entity or None:
        web3_keys = list(self._list.keys())
        _len = len(web3_keys)
        start_index: int = kwargs.get("start_index")
        provider_url: str = kwargs.get("provider_url")
        web3_callback_func = kwargs.get("func")
        if provider_url:
            start_index = web3_keys.index(provider_url)
        elif start_index is None or start_index >= _len:
            start_index = 0
        counter = start_index
        check = True
        result = None
        while check:
            _provider_url = web3_keys[counter]
            _web3_entity = self._list[_provider_url]
            measure_param = self._measure.measure(_web3_entity)
            if callable(web3_callback_func):
                web3_callback_func(_web3_entity, measure_param)
            if measure_param["isOk"]:
                result = _web3_entity
                check = False
            else:
                if counter < _len - 1:
                    counter = counter + 1
                else:
                    counter = 0
                if counter == start_index:
                    check = False
                    result = None
        return result

    def get_best_web3(self, **kwargs) -> Web3Entity or None:
        measure_data = self.measure_all(**kwargs)
        _result: Web3Entity or None = None
        _measure_param = None
        for _key in measure_data:
            temp_measure = measure_data[_key]["measure"]
            if temp_measure["isOk"]:
                if _measure_param:
                    if temp_measure["result"] < _measure_param:
                        _result = measure_data[_key]["item"]
                        _measure_param = temp_measure["result"]
                else:
                    _result = measure_data[_key]["item"]
                    _measure_param = temp_measure["result"]
        return _result
