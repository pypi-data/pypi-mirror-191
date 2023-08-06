import logging
import traceback
from typing import Dict, List, Tuple


def get_msg(e: Exception) -> str:
    return "".join(
        traceback.TracebackException.from_exception(e.__cause__).format()) if e.__cause__ is not None else str(
        e)


class SsdbResponseUtils:

    def __init__(self):
        raise Exception("Not allow to create a new intance of this class")

    @classmethod
    def encode_dict_to_pairs(cls, dict: Dict[any, any]) -> List[any]:
        pairs = []
        for k, v in dict.items():
            pairs.append(k)
            pairs.append(v)
        return pairs

    @classmethod
    def response_to_map(cls, response) -> Dict[bytes, bytes]:
        result_dict = {}
        for k, v in zip(response[::2], response[1::2]):
            result_dict[k] = v
        return result_dict

    @classmethod
    def response_to_str_map(cls, response) -> Dict[str, str]:
        result_dict = {}
        for k, v in zip(response[::2], response[1::2]):
            try:
                id = k.decode("utf-8")
                value = v.decode('utf-8')
                result_dict[id] = value
            except Exception as e:
                logging.error(f"response_to_str_map: {get_msg(e)}")

        return result_dict

    @classmethod
    def response_to_pair_list(cls, response) -> List[Tuple[bytes, bytes]]:
        return [
            (k, v)
            for k, v in zip(response[::2], response[1::2])
        ]

    @classmethod
    def to_str_map(cls, dict: Dict[bytes, bytes]) -> Dict[str, str]:
        result_dict = {}
        for k, v in dict.items():
            try:
                id = str(k.decode("utf-8"))
                value = str(v.decode('utf-8'))
                result_dict[id] = value
            except Exception as e:
                logging.error(f"to_str_map: {get_msg(e)}")

        return result_dict

    @classmethod
    def to_zset_score_dict(cls, response) -> Dict[str, float]:
        result_dict = {}
        for i, (k, v) in enumerate(zip(response[::2], response[1::2])):
            try:
                id = k.decode("utf-8")
                score = float(v.decode('utf-8'))
                result_dict[id] = score
            except Exception as e:
                logging.error(f"to_zset_score_dict: {get_msg(e)}")

        return result_dict

    @classmethod
    def to_rank_to_id_map(cls, response, ranks: List[int], start_rank: int) -> Dict[int, str]:
        result_dict = {}

        set_ranks = set(ranks)
        for i, (k, v) in enumerate(zip(response[::2], response[1::2])):
            try:
                id = k.decode("utf-8")
                score = float(v.decode('utf-8'))
                rank = start_rank + i
                if rank in set_ranks:
                    result_dict[start_rank + i] = id
            except Exception as e:
                logging.error(f"to_map: {get_msg(e)}")

        return result_dict
