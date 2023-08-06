class ChainId:
    BSC_MAINNET = 56
    FTM_MAINNET = 250
    ETH_MAINNET = 1


class _AppConfig:
    DEFAULT_NETWORK = {
        ChainId.BSC_MAINNET: {"maxTimestamp": 78},
        ChainId.ETH_MAINNET: {"maxTimestamp": 132},
        ChainId.FTM_MAINNET: {"maxTimestamp": 70},
    }


AppConfig = _AppConfig()
