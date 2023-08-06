from typing import List, Dict, Optional

from .base_ssdb import BaseSsdb
from .utils import SsdbResponseUtils


class BaseSsdbHash(BaseSsdb):

    def hincr(self, name: str, k: any, num: int) -> int:
        """
        Increase the given key value by num

        :param name: any
        :param k: any
        :param num
        :return:
        """
        pass

    def hset(self, name: str, k: any, v: any):
        pass

    def hget(self, name: str, k: any) -> Optional[bytes]:
        pass

    def hsize(self, name: str) -> int:
        pass

    def hexists(self, name: str, k: any) -> bool:
        pass

    def hdel(self, name: str, k: any):
        pass

    def hclear(self, name: str):
        pass

    def multi_hset(self, name: str, data: Dict[any, any]):
        pass

    def multi_hget(self, name: str, keys: List[str]) -> Dict[bytes, bytes]:
        pass

    def hkeys(self, name: str, key_start: any, key_end: any, limit: int) -> List[bytes]:
        pass

    def hlist(self, name_start: str, name_end: str, limit: int) -> List[str]:
        pass

    def hrlist(self, name_start: str, name_end: str, limit: int) -> List[str]:
        pass

    def hgetall(self, name: str) -> Dict[bytes, bytes]:
        pass


class SsdbHash(BaseSsdbHash):

    def hincr(self, name: str, k: any, num: int) -> int:
        result = self.execute_command('hincr', name, k, num)
        return int(result)

    def hset(self, name: str, k: any, v: any):
        self.execute_command('hset', name, k, v)

    def hget(self, name: str, k: any) -> Optional[bytes]:
        return self.execute_command('hget', name, k)

    def hsize(self, name: str) -> int:
        return int(self.execute_command('hsize', name))

    def hexists(self, name: str, k: any) -> bool:
        result = self.execute_command('hexists', name, k)
        return True if int(result) == 1 else False

    def hdel(self, name: str, k: any):
        self.execute_command('hdel', name, k)

    def hclear(self, name: str):
        self.execute_command('hclear', name)

    def multi_hset(self, name: str, data: Dict[any, any]):
        pairs = SsdbResponseUtils.encode_dict_to_pairs(data)
        self.execute_command('multi_hset', name, *pairs)

    def multi_hget(self, name: str, keys: List[str]) -> Dict[bytes, bytes]:
        result = self.execute_command('multi_hget', name, *keys)

        return SsdbResponseUtils.response_to_map(result)

    def hkeys(self, name: str, key_start: any, key_end: any, limit: int) -> List[bytes]:
        result = self.execute_command('hkeys', name, key_start, key_end, limit)
        return list(result)

    def hlist(self, name_start: str, name_end: str, limit: int) -> List[str]:
        result = self.execute_command('hlist', name_start, name_end, limit)
        return list(result)

    def hrlist(self, name_start: str, name_end: str, limit: int) -> List[str]:
        result = self.execute_command('hrlist', name_start, name_end, limit)
        return list(result)

    def hgetall(self, name: str) -> Dict[bytes, bytes]:
        result = self.execute_command('hgetall', name)
        return SsdbResponseUtils.response_to_map(result)
