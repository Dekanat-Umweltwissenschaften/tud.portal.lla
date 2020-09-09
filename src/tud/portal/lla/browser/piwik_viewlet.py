from plone.api.portal import get_tool
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class PiwikViewlet(ViewletBase):

    index = ViewPageTemplateFile('templates/piwik_viewlet.pt')

    def update(self):
        language = get_tool("portal_languages").getPreferredLanguage()
        self.iframe_url = "https://piwik.mz.tu-dresden.de/index.php?module=CoreAdminHome&action=optOut&language=" + language
