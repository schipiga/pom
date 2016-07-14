"""
Base UI element.

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

from selenium.common import exceptions
from selenium.webdriver import ActionChains

from pom.utils import Waiter

waiter = Waiter(polling=0.1)
presence_errors = (exceptions.StaleElementReferenceException,
                   exceptions.NoSuchElementException)


def wait_for_presence(func):
    """Decorator to wait for ui element will be present at display."""
    def wrapper(self, *args, **kwgs):
        self.wait_for_presence()
        return func(self, *args, **kwgs)

    return wrapper


def immediately(func):
    """Decorator to off selenium implicit waiting."""
    def wrapper(self, *args, **kwgs):
        try:
            self.webdriver.implicitly_wait(0)
            return func(self, *args, **kwgs)
        finally:
            self.webdriver.implicitly_wait(10)

    return wrapper


def register_ui(**ui):
    """Decorator to register ui elements of ui container."""
    def wrapper(cls):
        cls.register_ui(**ui)
        return cls

    return wrapper


def cache(func):
    """Decorator to cache instance method execution result."""
    attrname = '_cached_{}_{}'.format(func.__name__, id(func))

    def wrapper(self, *args, **kwgs):
        result = getattr(self, attrname, None)
        if not result:
            result = func(self, *args, **kwgs)
            setattr(self, attrname, result)
        return result

    return wrapper


class Container(object):
    """Container, base class."""

    @classmethod
    def register_ui(cls, **ui):
        """Register ui elements.

        Sets ui elements as cached properties. Inside property it clones ui
        element to provide safe-thread execution.
        """
        for ui_name, ui_obj in ui.iteritems():

            def ui_getter(self, ui_obj=ui_obj):
                ui_clone = ui_obj.clone()
                ui_clone.container = self
                return ui_clone

            ui_getter.__name__ = ui_name
            ui_getter = property(cache(ui_getter))
            setattr(cls, ui_name, ui_getter)

    def __enter__(self):
        """Allow use container as context manager for readable code."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit from context manager."""
        pass

    def find_element(self, locator):
        """Find DOM element inside container."""
        return self.webelement.find_element(*locator)

    def find_elements(self, locator):
        """Find DOM elements inside container."""
        return self.webelement.find_elements(*locator)


class WebElementProxy(object):
    """Web element proxy is used to catch exceptions with webelement."""

    def __init__(self, webelement_getter):
        """Constructor."""
        self._webelement_getter = webelement_getter
        self._cached_webelement = None

    def __getattr__(self, name):
        """Execute web element methods and properties."""
        def webelement_attr(self=self):
            self._cached_webelement = self._cached_webelement or \
                self._webelement_getter()
            return getattr(self._cached_webelement, name)

        try:
            result = webelement_attr()
        except presence_errors:
            self._cached_webelement = None
            result = webelement_attr()

        if not callable(result):
            return result

        def method(*args, **kwgs):
            try:
                return result(*args, **kwgs)
            except presence_errors:
                self._cached_webelement = None
                return webelement_attr()(*args, **kwgs)

        return method


class UI(object):
    """Base class of ui element."""

    container = None

    def __init__(self, *locator, **index):
        """Constructor.

        Arguments:
            - locator.
        """
        self.locator = locator
        self.index = index.get('index')

    @cache
    def __repr__(self):
        """Object representation."""
        return self.__class__.__name__ + \
            '(by={!r}'.format(self.locator[0]) + \
            ', value={!r}'.format(self.locator[1]) + \
            (')' if self.index is None else ', index={})'.format(self.index))

    @wait_for_presence
    def click(self):
        """Click ui element."""
        self.webelement.click()

    @wait_for_presence
    def right_click(self):
        """Right click ui element."""
        self._action_chains.context_click(self.webelement).perform()

    @wait_for_presence
    def double_click(self):
        """Double click ui element."""
        self._action_chains.double_click(self.webelement).perform()

    @property
    @wait_for_presence
    def value(self):
        """Get value of ui element."""
        return self.webelement.get_attribute('innerHTML').strip()

    @property
    @immediately
    def is_present(self):
        """Define is ui element present at display."""
        try:
            return self.webelement.is_displayed()
        except presence_errors:
            return False

    @property
    @immediately
    def is_enabled(self):
        """Define is ui element enabled."""
        return self.webelement.is_enabled()

    @property
    def webdriver(self):
        """Get webdriver."""
        return self.container.webdriver

    @property
    @cache
    def webelement(self):
        """Get webelement."""
        if self.index:
            webelement_getter = lambda self=self: \
                self.container.find_elements(self.locator)[self.index]

        else:
            webelement_getter = lambda self=self: \
                self.container.find_element(self.locator)

        return WebElementProxy(webelement_getter)

    @property
    def _action_chains(self):
        return ActionChains(self.webdriver)

    def clone(self):
        """Clone ui element."""
        return self.__class__(self.locator[0],
                              self.locator[1],
                              index=self.index)

    def wait_for_presence(self, timeout=5):
        """Wait for ui element presence."""
        if not waiter.exe(timeout, lambda: self.is_present):
            raise Exception("{!r} is still absent after {} sec".format(
                self, timeout))

    def wait_for_absence(self, timeout=5):
        """Wait for ui element absence."""
        if not waiter.exe(timeout, lambda: not self.is_present):
            raise Exception("{!r} is still present after {} sec".format(
                self, timeout))


class Block(UI, Container):
    """UI block is containerable ui element."""
