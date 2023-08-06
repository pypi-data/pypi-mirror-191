"""缓存

支持

"""

import sys
import pickle
import inspect
import hashlib
from pathlib import Path
from functools import wraps
from multiprocessing import Lock
from collections import OrderedDict
from typing import Any, Dict, Type, Union, Callable, List
from vxutils import vxtime, to_timestring, to_timestamp, to_json


__all__ = ["MissingCache", "CacheUnit", "DiskCacheUnit", "vxLRUCache"]
_ENDOFTIME = to_timestamp("2199-12-31 23:59:59")


class MissingCache(Exception):
    pass


class CacheUnit:
    def __init__(self, key: str, value: Any, expired_dt: float = None) -> None:
        self._key = key
        self._value = value
        self._expired_dt = to_timestamp(
            "2199-12-31 23:59:59" if expired_dt is None else expired_dt
        )
        self._is_expired = False

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> Any:
        return self._value

    @property
    def expired_dt(self) -> float:
        return self._expired_dt

    @property
    def size(self) -> float:
        return sys.getsizeof(self._value)

    @property
    def is_expired(self) -> float:
        if not self._is_expired:
            self._is_expired = self._expired_dt < vxtime.now()

        return self._is_expired

    def __str__(self) -> str:
        return (
            f"< {self.__class__.__name__} key: {self._key} value: {self._value} expired"
            f" at: {to_timestring(self.expired_dt)} > "
        )

    __repr__ = __str__

    def __getstate__(self) -> Dict:
        return {"key": self.key, "value": self.value, "expired_dt": self.expired_dt}

    def __setstate(self, state: Dict) -> None:
        self.__init__(**state)

    @classmethod
    def set_cache_params(cls, *args, **kwargs) -> None:
        pass

    @classmethod
    def init_cache(cls) -> OrderedDict:
        return OrderedDict()

    def clear(self) -> None:
        pass


class DiskCacheUnit(CacheUnit):
    _path = Path(".cache")

    def __init__(self, key: str, value: Any, expired_dt: float = 0) -> None:
        value_file = Path(self._path, f"{key}.pkl")
        with open(value_file, "wb") as f:
            pickle.dump({"key": key, "value": value, "expired_dt": expired_dt}, f)
        super().__init__(key, value_file.absolute(), expired_dt)

    @property
    def value(self) -> Any:
        with open(self._value, "rb") as f:
            cache_obj = pickle.load(f)
            return cache_obj["value"]

    @value.setter
    def value(self, value: Any) -> None:
        with open(self._value, "wb") as f:
            pickle.dump(
                {"key": self.key, "value": value, "expired_dt": self._expired_dt}, f
            )

    @property
    def size(self) -> float:
        return self._value.stat().st_size

    @classmethod
    def set_cache_params(cls, cache_dir: Union[str, Path]) -> None:
        cls._path = Path(cache_dir)
        Path(cls._path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def init_cache(cls) -> OrderedDict:
        if not Path(cls._path).exists():
            Path(cls._path).mkdir(parents=True, exist_ok=True)
            return OrderedDict()

        cache_objs = []
        for value_file in cls._path.glob("*.pkl"):
            with open(value_file, "rb") as fp:
                cache_params = pickle.load(fp)
                cache_objs.append(cls(**cache_params))

        return OrderedDict(
            {
                cache_obj.key: cache_obj
                for cache_obj in sorted(cache_objs, key=lambda x: x._expired_dt)
            }
        )

    def clear(self) -> None:
        self._value.unlink(missing_ok=True)


class vxLRUCache:
    """Cache"""

    def __init__(
        self,
        size_limit: float = 0,
        ttl: float = 0,
        unit_factory: Type[CacheUnit] = None,
    ):
        self._lock = Lock()
        self.size_limit = size_limit * 1000  # M
        self._ttl = ttl
        self._size = 0
        self._unit_factory = unit_factory or CacheUnit
        self._storage = OrderedDict()
        for key, cache_obj in self._unit_factory.init_cache().items():
            self.__setitem__(key, cache_obj)

    @property
    def storage(self) -> Dict:
        return {
            key: cache_obj
            for key, cache_obj in self._storage.items()
            if not cache_obj.is_expired
        }

    def keys(self) -> List[str]:
        return [
            key for key, cache_obj in self._storage.items() if not cache_obj.is_expired
        ]

    def __setitem__(self, key, value):
        expired_dt = vxtime.now() + self._ttl if self._ttl > 0 else _ENDOFTIME

        cache_obj = (
            value
            if isinstance(value, CacheUnit)
            else self._unit_factory(key, value, expired_dt)
        )
        # precalculate the size after od.__setitem__
        with self._lock:
            self._adjust_size(key, cache_obj)
            self._storage[key] = cache_obj
            self._storage.move_to_end(key)

        if self.limited:
            # pop the oldest items beyond size limit
            while self._size > self.size_limit:
                self.popitem(last=False)

    def __getitem__(self, key):
        v = self._storage.get(key, None)
        if v is None or v.is_expired:
            raise MissingCache(key)
        self._storage.move_to_end(key)
        return v.value

    def __contains__(self, key):
        return any(
            (not cache_obj.is_expired) and _key == key
            for _key, cache_obj in self._storage.items()
        )

    def __len__(self):
        return sum(self._storage)

    def __repr__(self):
        storage_string = "".join(
            f"\t== {cache_obj}\n" for cache_obj in list(self.storage.values())[-5:]
        )
        return (
            f"{self.__class__.__name__}<size_limit:{self.size_limit if self.limited else 'no limit'} total_size:{self.total_size}>\n{storage_string}"
        )

    def set_limit_size(self, limit):
        self.size_limit = limit

    @property
    def limited(self):
        """whether memory cache is limited"""
        return self.size_limit > 0

    @property
    def total_size(self):
        return self._size

    def clear(self):
        with self._lock:
            self._size = 0
            for cache_obj in self._storage.values():
                cache_obj.clear()
            self._storage.clear()

    def popitem(self, last=False):
        if len(self._storage) == 0:
            return None, None

        with self._lock:
            k, v = self._storage.popitem(last=last)
            self._size -= v.size
            v.clear()

        return k, v

    def pop(self, key, default=None):
        if key not in self._storage:
            return default

        with self._lock:
            v = self._storage[key]
            self._size -= v.size
            v.clear()
        return default if v.is_expired else v.value

    def _adjust_size(self, key, cache_obj):
        if key in self._storage:
            self._size -= self._storage[key].size

        self._size += cache_obj.size

    def __call__(self, func: Callable) -> Any:
        def wapper(*args, **kwargs):
            try:
                ba = inspect.signature(func).bind(*args, **kwargs)
                ba.apply_defaults()
                string = to_json(ba.arguments, sort_keys=True, default=str)
                key = hashlib.md5(string.encode()).hexdigest()
                retval = self.__getitem__(key)
            except MissingCache:
                retval = func(*args, **kwargs)
                self.__setitem__(key, retval)

            return retval

        return wapper

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__setitem__(key, value)


diskcache = vxLRUCache(size_limit=1000, unit_factory=DiskCacheUnit)
