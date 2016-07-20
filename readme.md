POM - Page Object Model micro-framework to develop UI tests easy, quickly and with pleasure.

Example of usage is in https://github.com/sergeychipiga/horizon_autotests

## IRL usage examples:

#### Page components declaration

```python
from pom import ui
from selenium.webdriver.common.by import By

from horizon_autotests.app import ui as _ui

from ..base import PageBase
from ..instances.page_instances import FormLaunchInstance
from ..volumes.tab_volumes import FormCreateVolume


@ui.register_ui(
    item_create_volume=ui.UI(
        By.CSS_SELECTOR, '[id$="action_create_volume_from_image"]'),
    item_update_metadata=ui.UI(
        By.CSS_SELECTOR, '[id$="action_update_metadata"]'))
class DropdownMenu(_ui.DropdownMenu):
    """Dropdown menu for image row."""


@ui.register_ui(
    checkbox=_ui.CheckBox(By.CSS_SELECTOR, 'input[type="checkbox"]'),
    dropdown_menu=DropdownMenu(),
    link_image=ui.Link(By.CSS_SELECTOR, 'td > a'))
class RowImage(_ui.Row):
    """Row with image in images table."""

    transit_statuses = ('Queued', 'Saving')


class TableImages(_ui.Table):
    """Images table."""

    columns = {'name': 2, 'type': 3, 'status': 4, 'format': 7}
    row_cls = RowImage


@ui.register_ui(
    checkbox_protected=_ui.CheckBox(By.NAME, 'protected'),
    combobox_disk_format=ui.ComboBox(By.NAME, 'disk_format'),
    combobox_source_type=ui.ComboBox(By.NAME, 'source_type'),
    field_image_file=ui.TextField(By.NAME, 'image_file'),
    field_image_url=ui.TextField(By.NAME, 'image_url'),
    field_min_disk=ui.TextField(By.NAME, 'minimum_disk'),
    field_min_ram=ui.TextField(By.NAME, 'minimum_ram'),
    field_name=ui.TextField(By.NAME, 'name'))
class FormCreateImage(_ui.Form):
    """Form to create image."""


@ui.register_ui(
    field_metadata_name=ui.UI(By.CSS_SELECTOR, '[ng-bind$="item.leaf.name"]'),
    field_metadata_value=ui.TextField(By.CSS_SELECTOR,
                                      '[ng-model$="item.leaf.value"]'))
class RowMetadata(_ui.Row):
    """Row of added metadata."""


class ListMetadata(ui.List):
    """List of added metadata."""

    row_cls = RowMetadata
    row_xpath = './li[contains(@ng-repeat, "item in existingList")]'


@ui.register_ui(
    button_add_metadata=ui.Button(By.CSS_SELECTOR, '[ng-click*="addCustom"]'),
    field_metadata_name=ui.TextField(By.NAME, 'customItem'),
    list_metadata=ListMetadata(By.CSS_SELECTOR, 'ul[ng-form$="metadataForm"]'))
class FormUpdateMetadata(_ui.Form):
    """Form to update image metadata."""

    submit_locator = By.CSS_SELECTOR, '.btn[ng-click$="modal.save()"]'
    cancel_locator = By.CSS_SELECTOR, '.btn[ng-click$="modal.cancel()"]'


@ui.register_ui(
    checkbox_protected=_ui.CheckBox(By.NAME, 'protected'),
    field_name=ui.TextField(By.NAME, 'name'))
class FormUpdateImage(_ui.Form):
    """Form to update image."""


@ui.register_ui(
    button_create_image=ui.Button(By.ID, 'images__action_create'),
    button_delete_images=ui.Button(By.ID, 'images__action_delete'),
    button_public_images=ui.Button(By.CSS_SELECTOR, 'button[value="public"]'),
    form_create_image=FormCreateImage(By.ID, 'create_image_form'),
    form_create_volume=FormCreateVolume(
        By.CSS_SELECTOR, '[action*="volumes/create"]'),
    form_launch_instance=FormLaunchInstance(
        By.CSS_SELECTOR,
        'wizard[ng-controller="LaunchInstanceWizardController"]'),
    form_update_image=FormUpdateImage(By.ID, 'update_image_form'),
    form_update_metadata=FormUpdateMetadata(By.CSS_SELECTOR,
                                            'div.modal-content'),
    table_images=TableImages(By.ID, 'images'))
class PageImages(PageBase):
    """Images Page."""

    url = "/project/images/"
    navigate_items = 'Project', 'Compute', 'Images'
```

#### Page usage with steps

```python
import pom

from horizon_autotests import EVENT_TIMEOUT

from .base import BaseSteps

CIRROS_URL = ('http://download.cirros-cloud.net/0.3.1/'
              'cirros-0.3.1-x86_64-uec.tar.gz')


class ImagesSteps(BaseSteps):
    """Images steps."""

    def page_images(self):
        """Open images page if it isn't opened."""
        return self._open(self.app.page_images)

    @pom.timeit('Step')
    def create_image(self, image_name, image_url=CIRROS_URL, image_file=None,
                     disk_format='QCOW2', min_disk=None, min_ram=None,
                     protected=False, check=True):
        """Step to create image."""
        page_images = self.page_images()
        page_images.button_create_image.click()

        with page_images.form_create_image as form:
            form.field_name.value = image_name

            if image_file:
                form.combobox_source_type.value = 'Image File'
                form.field_image_file.value = image_file

            else:
                form.combobox_source_type.value = 'Image Location'
                form.field_image_url.value = image_url

            if min_disk:
                form.field_min_disk.value = min_disk

            if min_ram:
                form.field_min_ram.value = min_ram

            if protected:
                form.checkbox_protected.select()
            else:
                form.checkbox_protected.unselect()

            form.combobox_disk_format.value = disk_format
            form.submit()

        if check:
            self.close_notification('success')
            page_images.table_images.row(
                name=image_name).wait_for_status('Active')

    @pom.timeit('Step')
    def delete_image(self, image_name, check=True):
        """Step to delete image."""
        page_images = self.page_images()

        with page_images.table_images.row(
                name=image_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        page_images.form_confirm.submit()

        if check:
            self.close_notification('success')
            page_images.table_images.row(
                name=image_name).wait_for_absence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def delete_images(self, image_names, check=True):
        """Step to delete images."""
        page_images = self.page_images()

        for image_name in image_names:
            page_images.table_images.row(
                name=image_name).checkbox.select()

        page_images.button_delete_images.click()
        page_images.form_confirm.submit()

        if check:
            self.close_notification('success')
            for image_name in image_names:
                page_images.table_images.row(
                    name=image_name).wait_for_absence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def update_metadata(self, image_name, metadata, check=True):
        """Step to update image metadata."""
        page_images = self.page_images()
        with page_images.table_images.row(
                name=image_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_update_metadata.click()

        with page_images.form_update_metadata as form:
            for metadata_name, metadata_value in metadata.items():
                form.field_metadata_name.value = metadata_name
                form.button_add_metadata.click()
                form.list_metadata.row(
                    metadata_name).field_metadata_value.value = metadata_value

            form.submit()

        if check:
            page_images.table_images.row(
                name=image_name, status='Active').wait_for_presence()
```


### About implicit_wait

As you see, I don't use implicit_wait. That's because it's really implicit :) And another case, implicit_wait waits until object will be present even if invisibile, but architecturally for user cases "present" means "visible". Difficult imagine a case when user need manipulate with invisible UI element via DOM in debug console to make something in application. Hmm, if it is, seems something is wrong with application developers.
