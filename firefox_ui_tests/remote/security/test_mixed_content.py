# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.testcase import FirefoxTestCase


class TestMixedContent(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        self.url = 'https://mozqa.com/data/firefox/security/mixedcontent.html'

    def test_mixed_content(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate(self.url)

        self.assertTrue('identity-icons-https-mixed-display' in
                        self.navbar.locationbar.favicon.value_of_css_property('list-style-image'))
        identity_popup = self.navbar.locationbar.identity_popup
        identity_popup.box.click()

        self.wait_for_condition(lambda _: identity_popup.popup.is_displayed())
        self.assertEqual(identity_popup.encryption_label.text,
                         self.browser.get_property('identity.broken_loaded'))
