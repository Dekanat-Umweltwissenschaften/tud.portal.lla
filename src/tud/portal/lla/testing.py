# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import tud.portal.lla


class TudPortalLlaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=tud.portal.lla)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tud.portal.lla:default')


TUD_PORTAL_LLA_FIXTURE = TudPortalLlaLayer()


TUD_PORTAL_LLA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TUD_PORTAL_LLA_FIXTURE,),
    name='TudPortalLlaLayer:IntegrationTesting'
)


TUD_PORTAL_LLA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TUD_PORTAL_LLA_FIXTURE,),
    name='TudPortalLlaLayer:FunctionalTesting'
)


TUD_PORTAL_LLA_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TUD_PORTAL_LLA_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='TudPortalLlaLayer:AcceptanceTesting'
)
