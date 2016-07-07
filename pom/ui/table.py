"""
POM table block.

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

from selenium.webdriver.common.by import By

from .base import Block


class Row(Block):
    """Row of table."""

    @property
    def cells(self):
        locator = By.XPATH, './/{}'.format(self.container.cell_tag)
        _cells = []

        for index, element in enumerate(self.find_elements(locator)):
            if element.is_displayed():
                cell = Block(locator[0], locator[1], index=index)
                cell.container = self
                _cells.append(cell)

        return _cells

    def cell(self, name):
        """Get cell of table.

        Arguments:
            - name: string, name of column.
        """
        position = self.container.columns[name]
        cell_selector = './/{}[{}]'.format(self.container.cell_tag, position)
        cell = Block(By.XPATH, cell_selector)
        cell.container = self
        return cell


class Table(Block):
    """Table."""

    row_cls = Row
    body_tag = "tbody"
    row_tag = "tr"
    cell_tag = "td"
    columns = None

    @property
    def rows(self):
        locator = By.XPATH, './/{}//{}'.format(self.body_tag or '.',
                                               self.row_tag)
        _rows = []

        for index, element in enumerate(self.find_elements(locator)):
            if element.is_displayed():
                row = self.row_cls(locator[0], locator[1], index=index)
                row.container = self
                _rows.append(row)

        return _rows

    def row(self, **kwgs):
        """Get row of table."""
        row = self.row_cls(By.XPATH, self._row_selector(**kwgs))
        row.container = self
        return row

    def _row_selector(self, **kwgs):
        pos_tmpl = '[position()={} and contains(., "{}")]'
        cell_selectors = []
        for name, value in kwgs.items():
            position = self.columns[name]
            cell_selectors.append(
                self.cell_tag + pos_tmpl.format(position, value))

        return './/{}//{}[{}]'.format(self.body_tag or '.',
                                      self.row_tag,
                                      " and ".join(cell_selectors))
