from typing import List, Dict, Optional

from .base_ssdb import BaseSsdb
from .utils import SsdbResponseUtils


class BaseSsdbKV(BaseSsdb):

    def set(self, key: any, value: any, ttl: int = -1):
        pass

    def exists(self, key: any) -> bool:
        pass

    def get(self, key: any) -> Optional[bytes]:
        pass

    def ttl(self, key: any) -> int:
        pass

    def incr(self, key: any, num: int) -> int:
        pass

    def remove(self, key: any):
        pass

    def multi_set(self, kv_dict: Dict[any, any]):
        pass

    def multi_get(self, keys: List[any]) -> Dict[bytes, bytes]:
        pass

    def multi_del(self, keys: List[any]):
        pass


class SsdbKV(BaseSsdbKV):

    def set(self, key: any, value: any, ttl: int = -1):
        if ttl is None or ttl <= 0:
            self.execute_command('set', key, value)
        else:
            self.execute_command('setx', key, value, ttl)

    def exists(self, key: any) -> bool:
        result = self.execute_command('exists', key)
        return True if int(result) == 1 else False

    def get(self, key: any) -> Optional[bytes]:
        return self.execute_command('get', key)

    def ttl(self, key: any) -> int:
        return int(self.execute_command('ttl', key))

    def incr(self, key: any, num: int) -> int:
        result = self.execute_command('incr', key, num)
        return int(result)

    def remove(self, key: any):
        self.execute_command('del', key)

    def multi_set(self, kv_dict: Dict[any, any]):
        pairs = SsdbResponseUtils.encode_dict_to_pairs(kv_dict)
        self.execute_command('multi_set', *pairs)

    def multi_get(self, keys: List[any]) -> Dict[bytes, bytes]:
        result = self.execute_command('multi_get', *keys)

        return SsdbResponseUtils.response_to_map(result)

    def multi_del(self, keys: List[any]):
        self.execute_command('multi_del', *keys)
