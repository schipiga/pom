"""
POM utils.

@author: chipiga86@gmail.com
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import logging
import time

__all__ = [
    'cache',
    'sleep',
    'timeit'
]

TIMEIT_LOG = logging.getLogger('timeit')
LOGGER = logging.getLogger(__name__)


def cache(func):
    """Decorator to cache instance method execution result."""
    attrname = '_cached_{}_{}'.format(func.__name__, id(func))

    @functools.wraps(func)
    def wrapper(self, *args, **kwgs):
        result = getattr(self, attrname, None)
        if not result:
            result = func(self, *args, **kwgs)
            setattr(self, attrname, result)
        return result

    return wrapper


def timeit(type_name):
    """Decorator to log function execution time."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwgs):
            start = time.time()
            try:
                return func(*args, **kwgs)
            finally:
                TIMEIT_LOG.debug(
                    "{} {!r} with args {!r} and kwargs {!r} took {:.4f}"
                    " second(s)".format(type_name or 'Function',
                                        func.__name__,
                                        args,
                                        kwgs,
                                        time.time() - start))
        return wrapper

    if callable(type_name):
        func = type_name
        type_name = None
        return decorator(func)
    else:
        return decorator


def sleep(seconds, message):
    """Sleep with message."""
    LOGGER.warn('Sleep {} second(s): {!r}'.format(seconds, message))
    time.sleep(seconds)
