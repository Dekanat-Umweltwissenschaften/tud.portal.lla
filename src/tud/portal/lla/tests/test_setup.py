# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from tud.portal.lla.testing import TUD_PORTAL_LLA_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that tud.portal.lla is properly installed."""

    layer = TUD_PORTAL_LLA_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tud.portal.lla is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'tud.portal.lla'))

    def test_browserlayer(self):
        """Test that ITudPortalLlaLayer is registered."""
        from tud.portal.lla.interfaces import (
            ITudPortalLlaLayer)
        from plone.browserlayer import utils
        self.assertIn(ITudPortalLlaLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TUD_PORTAL_LLA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['tud.portal.lla'])

    def test_product_uninstalled(self):
        """Test if tud.portal.lla is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'tud.portal.lla'))

    def test_browserlayer_removed(self):
        """Test that ITudPortalLlaLayer is removed."""
        from tud.portal.lla.interfaces import ITudPortalLlaLayer
        from plone.browserlayer import utils
        self.assertNotIn(ITudPortalLlaLayer, utils.registered_layers())
