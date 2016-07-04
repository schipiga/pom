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

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

from horizon_autotests.pom.utils import Waiter

waiter = Waiter(polling=0.1)


def wait_for_visibility(func):

    def wrapper(self, *args, **kwgs):
        if not self.webelement.is_displayed():
            if not waiter.exe(5, lambda: self.is_visible):
                raise Exception("{} is not visible", self.locator)
        return func(self, *args, **kwgs)

    return wrapper


def immediately(func):

    def wrapper(self, *args, **kwgs):
        try:
            self.webdriver.implicitly_wait(0)
            return func(self, *args, **kwgs)
        finally:
            self.webdriver.implicitly_wait(5)

    return wrapper


def register_ui(**ui):

    def wrapper(cls):
        cls.register_ui(**ui)
        return cls

    return wrapper


def cache(func):
    attrname = '_cached_' + func.__name__

    def wrapper(self, *args, **kwgs):
        result = getattr(self, attrname, None)
        if not result:
            result = func(self, *args, **kwgs)
            setattr(self, attrname, result)
        return result

    return wrapper


class Container(object):

    @classmethod
    def register_ui(cls, **ui):
        for ui_name, ui_obj in ui.iteritems():

            def ui_getter(self, ui_obj=ui_obj):
                ui_clone = ui_obj.clone()
                ui_clone.set_container(self)
                return ui_clone

            ui_getter.__name__ = ui_name
            ui_getter = property(cache(ui_getter))
            setattr(cls, ui_name, ui_getter)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def find_element(self, locator):
        return self.webelement.find_element(*locator)

    def find_elements(self, locator):
        return self.webelement.find_elements(*locator)


class WebElementProxy(object):

    def __init__(self, webelement_getter):
        self._webelement_getter = webelement_getter

    def __getattr__(self, name):

        try:
            result = getattr(self._webelement_getter(), name)
        except StaleElementReferenceException:
            result = getattr(self._webelement_getter(), name)

        if not callable(result):
            return result

        def method(*args, **kwgs):
            try:
                return result(*args, **kwgs)
            except StaleElementReferenceException:
                return getattr(self._webelement_getter(), name)(*args, **kwgs)

        return method


class UI(object):

    container = None

    def __init__(self, *locator):
        self.locator = locator

    def set_container(self, container):
        self.container = container

    @wait_for_visibility
    def click(self):
        self.webelement.click()

    @wait_for_visibility
    def right_click(self):
        self._action_chains.context_click(self.webelement).perform()

    @wait_for_visibility
    def double_click(self):
        self._action_chains.double_click(self.webelement).perform()

    @property
    @wait_for_visibility
    def value(self):
        return self.webelement.get_attribute('innerHTML').strip()

    @property
    @immediately
    def is_present(self):
        try:
            self.webelement.is_displayed()
            return True
        except Exception:
            return False

    @property
    @immediately
    def is_enabled(self):
        return self.webelement.is_enabled()

    @property
    @immediately
    def is_visible(self):
        return self.webelement.is_displayed()

    @property
    def webdriver(self):
        return self.container.webdriver

    @property
    def webelement(self):
        return WebElementProxy(
            lambda: self.container.find_element(self.locator))

    @property
    def _action_chains(self):
        return ActionChains(self.webdriver)

    def clone(self):
        return self.__class__(*self.locator)

    def wait_for_presence(self, timeout=5):
        if not waiter.exe(timeout, lambda: self.is_present):
            raise Exception("{!r} is absent".format(self.locator))

    def wait_for_absence(self, timeout=5):
        if not waiter.exe(timeout, lambda: not self.is_present):
            raise Exception("{!r} is present".format(self.locator))


class Block(UI, Container):
    pass
