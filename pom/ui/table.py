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

from .base import Block, register_ui


class _CellsMixin(object):

    @property
    def cells(self):
        locator = By.XPATH, self.cell_xpath
        _cells = []

        for index, element in enumerate(self.find_elements(locator)):
            if element.is_displayed():

                cell = self.cell_cls(locator[0], locator[1], index=index)
                cell.container = self
                _cells.append(cell)

        return _cells

    def cell(self, name):
        cell = self.cell_cls(By.XPATH, self._cell_selector(name))
        cell.container = self
        return cell

    def _cell_selector(self, name):
        position = self.container.columns[name]

        if self.cell_xpath.endswith(']'):
            return (self.cell_xpath.rstrip(']') +
                    ' and position()={}]'.format(position))
        else:
            return self.cell_xpath + '[{}]'.format(position)


class Row(Block, _CellsMixin):
    """Row of table."""

    cell_cls = Block
    cell_xpath = './/td'


class Header(Block, _CellsMixin):
    """Header of table."""

    cell_cls = Block
    cell_xpath = './/th'


class Body(Block):
    """Table body."""

    row_xpath = './/tr'

    @property
    def row_cls(self):
        """Row table class."""
        return self.container.row_cls

    @property
    def columns(self):
        """Table columns."""
        return self.container.columns

    @property
    def rows(self):
        """Visible rows of table."""
        locator = By.XPATH, self.row_xpath
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
                self.row_cls.cell_xpath + pos_tmpl.format(position, value))

        cell_selector = " and ".join(cell_selectors)

        if self.row_xpath.endswith(']'):
            return (self.row_xpath.rstrip(']') +
                    ' and {}]'.format(cell_selector))
        else:
            return self.row_xpath + '[{}]'.format(cell_selector)


class Footer(Block):
    """Table footer."""


@register_ui(
    header=Header(By.TAG_NAME, 'thead'),
    body=Body(By.TAG_NAME, 'tbody'),
    footer=Footer(By.TAG_NAME, 'tfoot'))
class Table(Block):
    """Table."""

    row_cls = Row
    columns = None

    @property
    def rows(self):
        """Table rows."""
        return self.body.rows

    def row(self, **kwgs):
        """Get row of table."""
        return self.body.row(**kwgs)
