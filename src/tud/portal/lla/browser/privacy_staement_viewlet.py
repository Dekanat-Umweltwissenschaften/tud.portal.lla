from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.api.portal import get_tool
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from tud.portal.lla.interfaces import IImprintPage

class PrivacyStatementViewlet(ViewletBase):

    index = ViewPageTemplateFile('templates/privacy_staement_viewlet.pt')

    def getImprintUrl(self):
        """Return one object that implements our IImprintPage interface."""

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        language = get_tool("portal_languages").getPreferredLanguage()
        imprints = catalog({'object_provides':IImprintPage.__identifier__, 'Language':language})

        if len(imprints) > 0:
            return imprints[0].getURL()
        else:
            return None