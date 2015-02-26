# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.testcase import FirefoxTestCase


class TestMixedContent(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.test_url = 'https://mozqa.com/data/firefox/security/mixedcontent.html'

    def test_mixed_content(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.test_url)

        favicon = self.browser.navbar.locationbar.favicon

        def check_favicon_image(self):
            favicon_image = self.execute_script("\
                return arguments[0].ownerDocument.defaultView\
                                   .getComputedStyle(arguments[0])\
                                   .getPropertyValue('list-style-image');\
            ", script_args=[favicon])
            return 'identity-icons-https-mixed-display' in favicon_image

        self.wait_for_condition(check_favicon_image)

        identity_popup = self.browser.navbar.locationbar.identity_popup
        identity_popup.box.click()

        self.wait_for_condition(lambda _: identity_popup.popup.is_displayed())
        self.assertEqual(identity_popup.encryption_label.text,
                         self.browser.get_property('identity.broken_loaded'))
