.. POM documentation master file, created by
   sphinx-quickstart on Fri Sep  9 15:12:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to POM's documentation!
===============================

==========
Annotation
==========
POM is Page-Object-Model microframework to develop web UI tests easy, quickly and with pleasure.

============
Architecture
============
POM provides API to manipulate with web UI elements and pages in browser. Under hood it uses selenium.
Before to act with UI element POM waits for its visibility, because in user cases user can't interact with UI element if it isn't visible at display.
POM provides tree hirarchy to request UI elements with UI caching mechanism at each level.

POM doesn't use **implicit_wait** method to wait UI element, because implicit_wait waits until element is present at DOM even if it isn't visible. And also implicit_wait has conflict with caching mechanism, that leads to long requests in some cases.

So POM has own implementation to wait element before interact. It leads to additinal webdriver request before interact with UI element, but provide reliable and simple architecture, without speed degradation.

============
How to start
============
Let imagine simple testcase:

- ``Go to https://facebook.com``
- ``Fill login / password fields with 'admin' / 'admin' values``
- ``Click button login``
- ``Assert page to log in is opened``
- ``Assert alert message is opened``

Its implementation with POM:

.. code:: python

 import unittest

 import pom
 from pom import ui
 from selenium.webdriver.common.by import By


 @ui.register_ui(field_login=ui.TextField(By.NAME, 'email'),
                 field_password=ui.TextField(By.NAME, 'pass'))
 class FormLogin(ui.Form):
     """Form to login."""


 @ui.register_ui(form_login=FormLogin(By.ID, 'login_form'))
 class PageMain(pom.Page):
     """Main page."""
     url = '/'


 @ui.register_ui(
     alert_message=ui.Block(By.CSS_SELECTOR, 'div.uiContextualLayerPositioner'))
 class PageLogin(pom.Page):
     """Login page."""
     url = '/login'


 @pom.register_pages([PageMain, PageLogin])
 class Facebook(pom.App):
     """Facebook web application."""
     def __init__(self):
         super(Facebook, self).__init__('https://www.facebook.com', 'firefox')
         self.webdriver.maximize_window()
         self.webdriver.set_page_load_timeout(30)


 class TestCase(unittest.TestCase):

     def setUp(self):
         self.fb = Facebook()
         self.addCleanup(self.fb.quit)

     def test_facebook_invalid_login(self):
         """User with invalid credentials can't login to facebook."""
         self.fb.page_main.open()
         with self.fb.page_main.form_login as form:
             form.field_login.value = 'admin'
             form.field_password.value = 'admin'
             form.submit()
         assert self.fb.current_page == self.fb.page_login
         assert self.fb.page_login.alert_message.is_present

**To launch example:**

- Save example code in file ``test_pom.py``
- Install POM framework ``pip install python-pom``
- Launch test example ``python -m unittest test_pom``

Full example of usage is in https://github.com/sergeychipiga/horizon_autotests.

====================
Supported components
====================

----------------------------
App (base application class)
----------------------------

.. autoclass:: pom.base.App
   :members:

----------------------
Page (base page class)
----------------------

.. autoclass:: pom.base.Page
   :members:

-----------------------
UI (base element class)
-----------------------

.. autoclass:: pom.ui.base.UI
   :members:

------
Button
------

.. autoclass:: pom.ui.button.Button
   :members:

--------
CheckBox
--------

.. autoclass:: pom.ui.checkbox.CheckBox
   :members:

--------
ComboBox
--------

.. autoclass:: pom.ui.combobox.ComboBox
   :members:

---------
TextField
---------

.. autoclass:: pom.ui.fields.TextField
   :members:

------------
IntegerField
------------

.. autoclass:: pom.ui.fields.IntegerField
   :members:

---------
FileField
---------

.. autoclass:: pom.ui.fields.FileField
   :members:

----
Form
----

.. autoclass:: pom.ui.form.Form
   :members:

----
Link
----

.. autoclass:: pom.ui.link.Link
   :members:

----
List
----

.. autoclass:: pom.ui.table.List
   :members:

-----
Table
-----

.. autoclass:: pom.ui.table.Table
   :members:

---
Row
---

.. autoclass:: pom.ui.table.Row
   :members:

------
Header
------

.. autoclass:: pom.ui.table.Header
   :members:

----
Body
----

.. autoclass:: pom.ui.table.Body
   :members:

------
Footer
------

.. autoclass:: pom.ui.table.Footer
   :members:
