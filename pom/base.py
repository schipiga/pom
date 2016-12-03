"""
POM base classes.

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

import logging
import re

from selenium import webdriver

from pom import ui
from pom import utils
from pom.exceptions import PomError

__all__ = [
    'App',
    'Page',
    'register_pages',
]

LOGGER = logging.getLogger(__name__)

browsers = {
    'chrome': webdriver.Chrome,
    'edge': webdriver.Edge,
    'firefox': webdriver.Firefox,
    'ie': webdriver.Ie,
    'opera': webdriver.Opera,
    'safari': webdriver.Safari,
    'phantom': webdriver.PhantomJS,
}


def register_pages(pages):
    """Decorator to register pages in application."""
    def wrapper(cls):
        """Wrapper to register pages."""
        cls._registered_pages.extend(pages)
        cls._registered_pages.sort(
            key=lambda page: len(page.url), reverse=True)

        for page in pages:
            func_name = utils.camel2snake(page.__name__)

            def page_getter(self, page=page):
                return page(self)

            page_getter.__name__ = func_name
            page_getter = property(utils.cache(page_getter))
            setattr(cls, func_name, page_getter)

        return cls

    return wrapper


class App(object):
    """Web application."""

    _registered_pages = []

    def __init__(self, url, browser, *args, **kwgs):
        """Constructor."""
        self.app_url = url.strip('/')
        LOGGER.info('Start {!r} browser'.format(browser))
        self.webdriver = browsers[browser](*args, **kwgs)

    def open(self, url):
        """Open url.

        Arguments:
            - url: string.
        """
        self.webdriver.get(self.app_url + url)

    def quit(self):
        """Close browser."""
        LOGGER.info('Close browser')
        self.webdriver.quit()

    @property
    def current_page(self):
        """Define current page"""
        current_url = self.webdriver.current_url
        for page in self._registered_pages:
            if re.match(self.app_url + page.url, current_url):
                return getattr(self, utils.camel2snake(page.__name__))
        else:
            raise PomError("Can't define current page")


class Page(ui.Container):
    """Page of web application."""

    url = None

    def __init__(self, app):
        """Constructor."""
        self.app = app
        self.webdriver = self.webelement = app.webdriver

    @utils.timeit
    def refresh(self):
        """Refresh page."""
        self.webdriver.refresh()

    @utils.timeit
    def open(self):
        """Open page."""
        self.app.open(self.url)

    @utils.timeit
    def forward(self):
        """Forward."""
        self.webdriver.forward()

    @utils.timeit
    def back(self):
        """Back."""
        self.webdriver.back()

    @property
    @utils.timeit
    def source(self):
        """Page source code."""
        return self.webdriver.page_source

    @utils.timeit
    def exec_js(self, js_code, async=False):
        """Execute javascript code."""
        if async:
            self.webdriver.execute_async_script(js_code)
        else:
            self.webdriver.execute_script(js_code)
