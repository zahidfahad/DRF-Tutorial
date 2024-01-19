from django.core.cache import cache




def set_cache(key: str, value: str, ttl: int) -> bool:
    try:
        cache.set(key, value, timeout=ttl)
    except Exception as err:
        return False
    return True


def get_cache(key: str) -> bool:
    try:
        return cache.get(key)
    except Exception as err:
        return False


def delete_cache(key: str) -> bool:
    try:
        cache.delete(key)
    except Exception as err:
        return False
    return True

