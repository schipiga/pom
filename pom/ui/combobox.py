"""
POM combobox.

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

from selenium.webdriver.support.ui import Select

from .base import UI, wait_for_presence
from ..utils import timeit


class ComboBox(UI):
    """Combobox."""

    @property
    @timeit
    @wait_for_presence
    def value(self):
        """Combobox value."""
        return self._select.first_selected_option \
            .get_attribute('innerHTML').strip()

    @value.setter
    @timeit
    @wait_for_presence
    def value(self, value):
        """Set combobox value."""
        if value in self.value:
            return

        for i, v in enumerate(self.values):
            if value in v:
                break
        else:
            raise Exception(
                '{!r} is absent among {} values'.format(value, self))

        self._select.select_by_index(i)

    @property
    @timeit
    @wait_for_presence
    def values(self):
        """Combobox values."""
        return [o.get_attribute('innerHTML').strip()
                for o in self._select.options]

    @property
    def _select(self):
        return Select(self.webelement)
