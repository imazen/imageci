from utils import hash


def test_hash_from_bytes():
    result = hash.hash_from_bytes(bytes([i for i in range(256)]))
    assert '1facbe8406cd904b' == result


# def test_hash_from_file():
#     result = hash.hash_from_file('hash_test_file')
#     assert '7982e9b2ef123fba' == result
