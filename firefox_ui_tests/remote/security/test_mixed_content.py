# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.testcase import FirefoxTestCase
from marionette_driver import Wait


class TestMixedContent(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://mozqa.com/data/firefox/security/mixedcontent.html'

    def tearDown(self):
        try:
            if self.browser.navbar.locationbar.identity_popup.is_open:
                self.browser.navbar.locationbar.identity_popup.close(force=True)
        finally:
            FirefoxTestCase.tearDown(self)

    def test_mixed_content(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        favicon = self.browser.navbar.locationbar.favicon
        self.wait_for_condition(lambda _: favicon.get_attribute('hidden') != 'none')
        self.assertTrue("identity-icons-https-mixed-display" in
                        favicon.value_of_css_property('list-style-image'))

        identity_popup = self.browser.navbar.locationbar.identity_popup
        identity_popup.box.click()

        Wait(self.marionette).until(lambda _: identity_popup.is_open)

        self.assertEqual(identity_popup.encryption_label.text,
                         self.browser.get_property('identity.broken_loaded'))

        identity_popup.close(force=True)
        self.assertFalse(identity_popup.is_open)
