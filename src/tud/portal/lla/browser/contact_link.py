from Products.Five.browser import BrowserView
from plone.api.portal import get_tool
from plone.memoize import view
from tud.portal.lla.contact import IContact
from Acquisition import aq_chain
from plone.app.multilingual.interfaces import ILanguageRootFolder
from Products.CMFCore.interfaces import ISiteRoot

class ContactLinkView(BrowserView):
    """Looks in the current language folder and try to find a contact object.
    """

    def _get_language_root_folder_path(self):
        for item in aq_chain(self.context):
            if ILanguageRootFolder.providedBy(item) or ISiteRoot.providedBy(item):
                return '/'.join(item.getPhysicalPath())
        return '/'

    @view.memoize
    def __call__(self):
        pc = get_tool('portal_catalog')
        results = pc({
            'path': {
                'query': self._get_language_root_folder_path(),
                'depth': 1
            },
            'object_provides': IContact.__identifier__,
            'sort_limit': 1

        })[:1]

        if results:
            return results[0].getURL()
        return None