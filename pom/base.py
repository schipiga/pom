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

from selenium import webdriver

from .ui import Container

__all__ = [
    'App',
    'Page'
]

browsers = {
    'firefox': webdriver.Firefox,
    'phantom': webdriver.PhantomJS,
    'Chrome': webdriver.Chrome,
}


class App(object):
    """Web application."""

    def __init__(self, url, browser, *args, **kwgs):
        """Constructor."""
        self.app_url = url.strip('/')
        self.webdriver = browsers[browser](*args, **kwgs)

    def open(self, url):
        """Open url.

        Arguments:
            - url: string.
        """
        self.webdriver.get(self.app_url + url)

    def quit(self):
        """Close browser."""
        self.webdriver.quit()


class Page(Container):
    """Page of web application."""

    url = None

    def __init__(self, app):
        """Constructor."""
        self.app = app
        self.webdriver = app.webdriver
        self.webelement = self.webdriver

    def refresh(self):
        """Refresh page."""
        self.webdriver.refresh()
