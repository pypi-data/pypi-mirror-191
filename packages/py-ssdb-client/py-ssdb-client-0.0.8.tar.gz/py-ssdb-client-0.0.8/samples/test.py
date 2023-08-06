from py_ssdb_client import SsdbClient


def run_test_simple_kv(client: SsdbClient):
    print('=========KEY-VALUE TESTING===========')
    key = 'simple_key'
    client.set(key, 'this is a sentence')
    result = client.get(key)
    print(f'Get: {result}')

    result = client.incr('k', 10)
    print(f'incr: {result}')

    client.remove(key)
    result = client.get(key)
    print(f'get after remove: {result}')
    assert result is None

    result = client.exists('k')
    print(f'exists: {result}')
    assert result == True

    result = client.exists(key)
    print(f'exists: {result}')
    assert result == False

    result = client.multi_set({'a': 1, 'b': 2})
    print(f'multi_set: {result}')
    result = client.multi_get(['a', 'b'])
    print(f'multi_get: {result}')


def run_test_hash(client: SsdbClient):
    print('=========HASH TESTING===========')
    name = "hash"

    client.multi_hset(name, {'a': 34, 'b': 14, 'c': 100})
    client.hset(name, 's', 33)

    result = client.multi_hget(name, ['a', 'c', 's'])
    print(f'multi_hget: {result}')
    result = client.multi_hget('hash15', ['a', 'c'])
    print(f'multi_hget: {result}')

    result = client.hdel(name, 's')
    result = client.hget(name, 's')
    print(f'hget: {int(result) if result is not None else ""}')

    result = client.hsize(name)
    print(f'hsize: {int(result) if result is not None else ""}')

    result = client.hsize('hash15')
    print(f'hsize: {int(result) if result is not None else ""}')

    result = client.hexists('hash15', 'a')
    print(f'hexists: {result if result is not None else ""}')
    assert result == False

    print('Test HIncr')
    client.hset('hash_incr', 'a', 1)
    client.hincr('hash_incr', 'a', 100)
    result = client.hget('hash_incr', 'a')
    print(f'hash_incr: {int(result) if result is not None else ""}')

    result = client.hkeys(name,'a', 'z', 10)
    print(f'hkeys: {result if result is not None else ""}')

    result = client.hgetall(name)
    print(f'hgetall: {result if result is not None else ""}')


def run_test_sorted_set(client: SsdbClient):
    print('=========SORTED SET TESTING===========')
    client.multi_zset('sorted_set', {'a': 34, 'b': 14, 'c': 100})
    result = client.multi_zget('sorted_set', ['a', 'c', 's'])
    print(f'sorted_set: {result}')

    result = client.zrange('sorted_set', 0, 2)
    print(f'zrange: {result}')
    result = client.zrrange('sorted_set', 0, 2)
    print(f'zrrange: {result}')


if __name__ == "__main__":
    client = SsdbClient(
        host="127.0.0.1",
        port=8888
    )

    client.auth('sadsdgv')
    run_test_simple_kv(client)
    run_test_hash(client)
    run_test_sorted_set(client)
