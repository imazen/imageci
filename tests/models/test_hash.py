from models import hash


def test_hash_from_bytes():
    result = hash.hash_from_bytes(bytes([i for i in range(256)]))
    assert 'abcd' == result
