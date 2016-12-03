"""
---------
POM utils
---------
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
import inspect
import logging
import time

__all__ = [
    'cache',
    'camel2snake',
    'log',
]

LOGGER = logging.getLogger(__name__)


def cache(func):
    """Decorator to cache instance method execution result.

    Note:
        It implements ordinary approach to cache function execution result.
        But also it uses as key not only function name but its id too.
        It's related with inheritance specific, like that:

        .. code:: python

            class A(object):

                @cache
                def meth(self):
                    pass

            class B(A):

                @cache
                def meth(self):
                    pass

                @cache
                def _meth(self):
                    super(A, self).meth()
    """
    attrname = '_cached_{}_{}'.format(func.__name__, id(func))

    @functools.wraps(func)
    def wrapper(self, *args, **kwgs):
        result = getattr(self, attrname, None)
        if not result:
            result = func(self, *args, **kwgs)
            setattr(self, attrname, result)
        return result

    return wrapper


def camel2snake(string):
    """Camel case to snake case converter."""
    return ''.join('_{}'.format(s.lower()) if s.isupper() else s
                   for s in string).strip('_')


def log(func):
    """Decorator to log function with arguments and execution time.

    Note:
        It rejects ``self`` arguments from log messages.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwgs):
        # reject self from log args if it is present
        __tracebackhide__ = True
        log_args = _reject_self_from_args(func, args)

        func_name = getattr(func, '__name__', str(func))
        LOGGER.debug(
            'Function {!r} starts with args {!r} and kwgs {!r}'.format(
                func_name, log_args, kwgs))
        start = time.time()
        try:
            result = func(*args, **kwgs)
        finally:
            LOGGER.debug('Function {!r} ended in {:.4f} sec'.format(
                func_name, time.time() - start))
        return result

    return wrapper


def get_unwrapped_func(func):
    """Get original function under decorator.

    Decorator hides original function inside itself. But in some cases it's
    important to get access to original function, for ex: for documentation.

    Args:
        func (function): function that can be potentially a decorator which
            hides original function

    Returns:
        function: unwrapped function or the same function
    """
    if not inspect.isfunction(func) and not inspect.ismethod(func):
        return func

    if func.__name__ != func.func_code.co_name:
        for cell in func.func_closure:
            obj = cell.cell_contents
            if inspect.isfunction(obj):
                if func.__name__ == obj.func_code.co_name:
                    return obj
                else:
                    return get_unwrapped_func(obj)
    return func


def _reject_self_from_args(func, args):
    func_name = getattr(func, '__name__', str(func))
    args = list(args)
    if args:
        arg = args[0]
        im_func = getattr(getattr(arg, func_name, None), 'im_func', None)
        if get_unwrapped_func(im_func) is get_unwrapped_func(func):
            args.remove(arg)
    return args
