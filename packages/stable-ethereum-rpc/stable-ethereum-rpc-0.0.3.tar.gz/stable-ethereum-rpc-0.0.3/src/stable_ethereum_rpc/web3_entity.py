import time

from web3 import Web3
from web3.middleware import geth_poa_middleware


class SimpleWeb3Entity:
    def __init__(self, provider_url: str, rpc_type: str = None):
        self.provider_url = provider_url
        self.rpc_type = rpc_type if rpc_type else "http"


class Web3Entity:
    def __init__(self, provider_url: str, rpc_type: str, chain_id: int):
        self.provider_url = provider_url
        self.rpc_type = rpc_type
        self.chain_id = chain_id
        self._web3: Web3 = Web3Entity.create_web3_provider(self.provider_url, self.rpc_type)
        self._sleep: int or None = None
        self.error = None

    def is_available(self) -> bool:
        return self._sleep is not None

    def _check_available(self) -> bool:
        if self._sleep:
            current_timestamp = time.time()
            if current_timestamp <= self._sleep:
                self._sleep = None
                self.error = None
                return True
            else:
                return False
        else:
            return True

    def _take_a_nap(self):
        if self._sleep is None:
            current_timestamp = time.time()
            self._sleep = current_timestamp + 300

    def get_block(self, block_identifier, full_transactions: bool = False):
        is_available = self._check_available()
        if is_available:
            try:
                return self._web3.eth.get_block(block_identifier, full_transactions)
            except Exception as error:
                self.error = error
                self._take_a_nap()
                return False
        return False

    @staticmethod
    def create_http_provider(provider_url: str) -> Web3:
        _web3 = Web3(Web3.HTTPProvider(provider_url, request_kwargs={"timeout": 1}))
        _web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return _web3

    @staticmethod
    def create_ipcp_provider(provider_url: str) -> Web3:
        _web3 = Web3(Web3.IPCProvider(provider_url))
        return _web3

    @staticmethod
    def create_websocket_provider(provider_url: str) -> Web3:
        _web3 = Web3(Web3.WebsocketProvider(provider_url))
        return _web3

    @staticmethod
    def create_web3_provider(provider_url: str, _type: str) -> Web3 or None:
        if _type == "http":
            return Web3Entity.create_http_provider(provider_url)
        elif _type == "ipcp":
            return Web3Entity.create_ipcp_provider(provider_url)
        elif _type == "websocket":
            return Web3Entity.create_websocket_provider(provider_url)
        raise Exception(f"Invalid type: {_type}")
