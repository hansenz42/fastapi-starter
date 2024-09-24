import uuid


def gen_uuid():
    return uuid.uuid1().hex


__all__ = [gen_uuid]
