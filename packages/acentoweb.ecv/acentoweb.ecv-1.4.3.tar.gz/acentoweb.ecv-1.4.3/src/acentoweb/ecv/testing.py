# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import acentoweb.ecv


class AcentowebEcvLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=acentoweb.ecv)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'acentoweb.ecv:default')


ACENTOWEB_CVE_FIXTURE = AcentowebEcvLayer()


ACENTOWEB_CVE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ACENTOWEB_CVE_FIXTURE,),
    name='AcentowebEcvLayer:IntegrationTesting',
)


ACENTOWEB_CVE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ACENTOWEB_CVE_FIXTURE,),
    name='AcentowebEcvLayer:FunctionalTesting',
)


ACENTOWEB_CVE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ACENTOWEB_CVE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='AcentowebEcvLayer:AcceptanceTesting',
)
