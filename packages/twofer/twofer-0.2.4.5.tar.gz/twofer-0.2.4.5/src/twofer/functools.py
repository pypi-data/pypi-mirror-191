import os
from sys import stderr
from calendar import timegm
from collections.abc import Callable
from time import gmtime
from typing import Any


_FUNCTOOLS_DEBUG = bool(os.environ.get('_FUNCTOOLS_DEBUG'))


def time_limited_cache(expires_sec: int, /) -> Callable:

    def decorating_function(user_function: Callable, /) -> Callable:

        cache: dict[Any, tuple[int, Any]] = {}

        def wrapper(*args, **kwds) -> Any | None:

            sec =  timegm(gmtime())
            key = (*args, *tuple(sorted(kwds.items())))
            if key in cache and sec < cache[key][0]:
                if _FUNCTOOLS_DEBUG:
                    print(f'time_limited_cache: use cache ({user_function.__name__}{key})',
                        file=stderr)
                result = cache[key][1]
            else:
                result = user_function(*args, **kwds)
                cache[key] = (sec + expires_sec, result)
            return result

        return wrapper

    return decorating_function
