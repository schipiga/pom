"""
POM Fields.

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

from .base import UI, wait_for_presence
from ..utils import timeit


class TextField(UI):
    """Text field."""

    @property
    @timeit
    @wait_for_presence
    def value(self):
        """Value of text field."""
        return self.webelement.text or self.webelement.get_attribute('value')

    @value.setter
    @timeit
    @wait_for_presence
    def value(self, text):
        """Set value of text field."""
        self.webelement.clear()
        self.webelement.send_keys(text)


class IntegerField(UI):
    """Integer field."""

    @property
    @timeit
    @wait_for_presence
    def value(self):
        """Value of integer field."""
        return self.webelement.get_attribute('value')

    @value.setter
    @timeit
    @wait_for_presence
    def value(self, text):
        """Set value of integer field."""
        self.webelement.clear()
        self.webelement.send_keys(text)


class FileField(UI):
    """File field."""

    @property
    @timeit
    @wait_for_presence
    def value(self):
        """Value of text field."""
        return self.webelement.text

    @value.setter
    @timeit
    @wait_for_presence
    def value(self, text):
        """Set value of text field."""
        self.webelement.clear()
        self.webelement.send_keys(text)
