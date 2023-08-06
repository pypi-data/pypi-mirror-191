import bcrypt


def bytes_to_string(value: bytes) -> str:
    return value.decode('utf-8')


def string_to_bytes(value: str) -> bytes:
    return value.encode('utf-8')


def get_hash(password: str) -> bytes:
    """
    Get a password string and return a hash.
    :param password:
    :return: hash
    """
    hashed = bcrypt.hashpw(string_to_bytes(password), bcrypt.gensalt())
    return hashed


def check_hash(password: bytes, hashed: bytes):
    return bcrypt.checkpw(password, hashed)


def check_password(password: str, hashed: str):
    return check_hash(string_to_bytes(password), string_to_bytes(hashed))