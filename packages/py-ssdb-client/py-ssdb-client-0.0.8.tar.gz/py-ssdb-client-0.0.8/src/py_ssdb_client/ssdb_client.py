import json
from typing import Dict, Union

import pyssdb

from .ssdb_hash import SsdbHash
from .ssdb_kv import SsdbKV
from .ssdb_sorted_set import SsdbSortedSet
from .utils import SsdbResponseUtils


#
# @author anhlt
#
class SsdbClient(SsdbKV, SsdbHash, SsdbSortedSet):

    def __init__(self, host: str, port: int):
        # TODO: Replace this client to fixed connection pool properly
        self.ssdb: pyssdb.Client = pyssdb.Client(host, port)

        info = self.info()
        print('SSDB info:')
        print(json.dumps(info, ensure_ascii=False, indent=2))

    def auth(self, password: str) -> bool:
        result = self.ssdb.execute_command('auth', password)
        return True if int(result) == 1 else False

    def info(self) -> Dict[str, str]:
        result_dict = self.ssdb.execute_command('info')
        return SsdbResponseUtils.to_str_map(result_dict)

    def dbsize(self) -> int:
        result_dict = self.ssdb.execute_command('dbsize')
        return int(result_dict)

    def execute_command(self, cmd: str, *args) -> Union[None, list, int, bool]:
        return self.ssdb.execute_command(cmd, *args)
