# -*- coding: utf-8 -*-
from acentoweb.ecv.testing import ACENTOWEB_CVE_FUNCTIONAL_TESTING
from acentoweb.ecv.testing import ACENTOWEB_CVE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = ACENTOWEB_CVE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_ecv_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='ecv-view'
        )
        self.assertTrue(view.__name__ == 'ecv-view')
        # self.assertTrue(
        #     'Sample View' in view(),
        #     'Sample View is not found in ecv-view'
        # )

    def test_ecv_view_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='ecv-view'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = ACENTOWEB_CVE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
