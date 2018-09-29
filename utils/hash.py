import xxhash

# If issues with this, use blake2  https://blake2.net/


def hash_from_file(filename: str) -> str:
    with open(filename, 'rb') as f:
        xxh = xxhash.xxh64(f.read())
    return xxh.hexdigest()


def hash_from_bytes(source: bytes) -> str:
    return xxhash.xxh64(source).hexdigest()
