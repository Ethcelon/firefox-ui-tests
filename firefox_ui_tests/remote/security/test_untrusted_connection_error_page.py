# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette import By, MarionetteException

from firefox_ui_harness.testcase import FirefoxTestCase


class TestUntrustedConnectionErrorPage(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.test_url = 'https://ssl-selfsigned.mozqa.com'

    def tearDown(self):
        FirefoxTestCase.tearDown(self)

    def test_untrusted_connection_error_page(self):
        # Test the GetMeOutOfHereButton from an Untrusted Error page
        with self.marionette.using_context('content'):
            self.assertRaises(MarionetteException,
                              self.marionette.navigate, self.test_url)
            # Wait for the DOM to receive events
            time.sleep(1)

            button = self.marionette.find_element(
                By.ID, "getMeOutOfHereButton")
            self.assertTrue(button.is_displayed())
            button.click()
            self.wait_for_condition(
                lambda mn: self.browser.default_homepage in mn.get_url())
