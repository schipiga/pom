"""
Presentable Interface.

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

from abc import ABCMeta
from functools import wraps
from logging import getLogger

log = getLogger(__name__)


class PresentableError(Exception):
    pass


def if_present(func):

    @wraps(func)
    def wrapper(self, *args, **kwgs):
        if self.is_present:
            return func(self, *args, **kwgs)
        else:
            log.error("{} is absent, skip {}".format(self.__class__.__name__,
                                                     func.__name__))

    return wrapper


def if_absent(func):

    @wraps(func)
    def wrapper(self, *args, **kwgs):
        if not self.is_present:
            return func(self, *args, **kwgs)
        else:
            log.error("{} is present, skip {}".format(self.__class__.__name__,
                                                      func.__name__))

    return wrapper


def must_present(func):

    @wraps(func)
    def wrapper(self, *args, **kwgs):
        if not self.is_present:
            raise PresentableError(
                '{} must be present before {}.'.format(self.__class__.__name__,
                                                       func.__name__))
        return func(self, *args, **kwgs)

    return wrapper


def must_absent(func):

    @wraps(func)
    def wrapper(self, *args, **kwgs):
        if self.is_present:
            raise PresentableError(
                '{} must be absent before {}.'.format(self.__class__.__name__,
                                                      func.__name__))
        return func(self, *args, **kwgs)

    return wrapper


class IPresentable(object):

    __metaclass__ = ABCMeta

    @property
    def is_present(self):
        """Object presence status.
        :Returns:
        True or False.
        """

    def wait_for_presence(self, timeout):
        """Waits until object will appear.
        :Args:
        - timeout - timeout value in seconds.
        :Raises:
        PresentableError - if object is still absent after timeout.
        """

    def wait_for_absence(self, timeout):
        """Waits until object will disappear.
        :Args:
        - timeout - timeout value in seconds.
        :Raises:
        PresentableError - if object is still present after timeout.
        """
