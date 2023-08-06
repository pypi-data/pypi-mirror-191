"""各种实时行情接口"""

from .tencent import vxTencentHQ
from .tdx import vxHqAPI

__all__ = ["vxTencentHQ", "vxHqAPI"]
