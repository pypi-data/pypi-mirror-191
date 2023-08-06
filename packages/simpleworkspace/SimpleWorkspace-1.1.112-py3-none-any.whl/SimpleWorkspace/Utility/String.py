import hashlib as _hashlib 
def Hash(data: str | bytes, hashFunc=_hashlib.sha256()) -> str:
    if type(data) == str:
        data = data.encode()
    hashFunc.update(data)
    return hashFunc.hexdigest()