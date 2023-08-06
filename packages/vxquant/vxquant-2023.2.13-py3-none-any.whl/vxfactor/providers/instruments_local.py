from vxfactor.providers import vxInstrumentsProvider


class LocalInstrumentsProvider(vxInstrumentsProvider):
    def __init__(self, datapath=".data") -> None:
        super().__init__(datapath)
