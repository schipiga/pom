"""
POM checkbox.

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

from .base import UI, immediately, wait_for_visibility


class CheckBox(UI):
    """Checkbox."""

    @property
    @immediately
    def is_selected(self):
        """Define is checkbox selected."""
        return self.webelement.is_selected()

    @wait_for_visibility
    def select(self):
        """Select checkbox if it isn't selected."""
        if not self.is_selected:
            self.webelement.click()

    @wait_for_visibility
    def unselect(self):
        """Unselect checkbox if it is selected."""
        if self.is_selected:
            self.webelement.click()
