import logging
from typing import Optional, Union

logger = logging.getLogger()


class ZplConfig:
    __slots__ = ['timeout', 'width', 'height', 'dpmm']

    def __init__(self,
                 timeout: Optional[int] = None,
                 width: Union[None, float, int] = None,
                 height: Union[None, float, int] = None,
                 dpmm: Union[None, float, int] = None):
        self.timeout: int = min(500, max(1, timeout if isinstance(timeout, int) else 10))
        self.width: float = float(min(100, max(1, width if isinstance(width, (int, float)) else 4)))
        self.height: float = float(min(100, max(1, height if isinstance(height, (int, float)) else 6)))
        self.dpmm: float = float(min(100, max(1, dpmm if isinstance(dpmm, (int, float)) else 8)))

    def copy(self) -> "ZplConfig":
        return ZplConfig(self.timeout, self.width, self.height, self.dpmm)
