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

from .base import UI


class ComboBox(UI):

    @property
    def webelement(self):
        return Select(super(ComboBox, self).webelement)

    @property
    def value(self):
        return self.webelement.first_selected_option.text

    @value.setter
    def value(self, value):
        self.webelement.select_by_visible_text(value)

    @property
    def values(self):
        return [o.text for o in self.webelement.options]
