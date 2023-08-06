import time
import timeit
from stable_ethereum_rpc.config import AppConfig
from stable_ethereum_rpc.web3_list import Web3Entity


class Web3Measure:
    def __init__(self, chain_id: int, max_timestamp: int = None):
        self.chain_id = chain_id
        if max_timestamp:
            self.max_timestamp = max_timestamp
        else:
            self.max_timestamp = AppConfig.DEFAULT_NETWORK[chain_id]["maxTimestamp"]

    def _timestamp(self, web3: Web3Entity):
        start_time = timeit.default_timer()
        _block_data = web3.get_block("latest")
        end_time = timeit.default_timer()
        time_to_run = end_time - start_time
        if _block_data:
            _timestamp = _block_data["timestamp"]
            current_timestamp = time.time()
            distance = current_timestamp - _timestamp
            return {
                "result": distance * distance * time_to_run,
                "distance": distance,
                "time": time_to_run,
                "isOk": 0 <= distance <= self.max_timestamp and time_to_run < 5,
                "error": None,
            }
        else:
            return {"result": None, "distance": None, "time": time_to_run, "isOk": False, "error": web3.error}

    def measure(self, web3: Web3Entity):
        return self._timestamp(web3)
