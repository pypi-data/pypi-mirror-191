from vxutils import vxWrapper, logger

_default_providers = {
    "current": {"class": "vxfactor.providers.hq_tdx.TdxHQProvider", "params": {}},
    "calendar": {
        "class": "vxfactor.providers.calendar_cn.CNCalenderProvider",
        "params": {},
    },
    "instruments": {
        "class": "vxfactor.providers.vxInstrumentsProvider",
        "params": {"inst_path": ".data/cn/instruments"},
    },
    "features": {
        "class": "vxfactor.providers.vxFeaturesProvider",
        "params": {"feature_path": ".data/cn/"},
    },
    "factors": {
        "class": "vafactor.providers.vxFactorsProvider",
        "params": {"data_path": "./data/cn"},
    },
}


class vxMdapi:
    def __init__(self, **providers):
        """一个供应商接口"""

        providers = dict(**_default_providers, **providers)
        self.register_providers(**providers)

    def register_providers(self, **providers):
        for name, provider in providers.items():
            if not provider:
                continue

            _provider = vxWrapper.init_by_config(provider)
            if not callable(_provider):
                logger.warning(f"{name} 的API接口无法调用 {_provider}.")
                continue
            self.__dict__[name] = _provider
            logger.info(f"注册{name}接口成功 {_provider}")


mdapi = vxMdapi()

if __name__ == "__main__":
    print(mdapi.calendar("2020-01-04", "2021-01-04"))
    print(mdapi.current("SHSE.600000"))
