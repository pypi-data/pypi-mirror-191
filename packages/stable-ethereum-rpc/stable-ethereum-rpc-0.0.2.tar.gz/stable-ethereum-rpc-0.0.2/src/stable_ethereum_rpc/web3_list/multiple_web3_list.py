from typing import List

from stable_ethereum_rpc.web3_entity import SimpleWeb3Entity, Web3Entity
from stable_ethereum_rpc.web3_list import BaseWeb3List


def _sort(item):
    return item["measure"]["result"]


def _map(item):
    return item["item"]


class MultipleWeb3List(BaseWeb3List):
    def __init__(self, chain_id: int, web3_list: List[SimpleWeb3Entity or str], **kwargs):
        super().__init__(chain_id, web3_list, **kwargs)
        _size = kwargs.get("size")
        self.selected_size = _size if _size else 2

    def get_sufficient_web3(self, **kwargs) -> List[Web3Entity]:
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
        result = []
        while check:
            _provider_url = web3_keys[counter]
            _web3_entity = self._list[_provider_url]
            measure_param = self._measure.measure(_web3_entity)
            if callable(web3_callback_func):
                web3_callback_func(_web3_entity, measure_param)
            if measure_param["isOk"]:
                result.append(_web3_entity)
                if len(result) == self.selected_size:
                    check = False
            if counter < _len - 1:
                counter = counter + 1
            else:
                counter = 0
            if counter == start_index:
                check = False
        return result

    def get_best_web3(self, **kwargs) -> List[Web3Entity]:
        measure_data = self.measure_all(**kwargs)
        data = list(measure_data.values())
        raw_result = []
        for item in data:
            if item["measure"]["isOk"]:
                raw_result.append(item)
        raw_result.sort(key=_sort)
        return list(map(_map, raw_result[0 : self.selected_size]))
