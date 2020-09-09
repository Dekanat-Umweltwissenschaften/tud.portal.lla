## @package tud.portal.lla
#  @author Paul Grunewald <paul.grunewald@tu-dresden.de>
#  @date 14.12.2016
#  @copyright TU Dresden
"""Add additional menu items
"""
from AccessControl import getSecurityManager
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces import ILanguage
from plone.app.multilingual.browser.menu import TranslateMenu as BaseTranslateMenu
from plone.app.multilingual.interfaces import LANGUAGE_INDEPENDENT, ITranslatable
from tud.portal.lla import _
from plone.app.multilingual.browser.utils import is_language_independent

class TranslateMenu(BaseTranslateMenu):
    def getMenuItems(self, context, request):
        menu = super(TranslateMenu, self).getMenuItems(context, request)

        url = context.absolute_url()

        is_neutral_content = (
            ILanguage(context).get_language() == LANGUAGE_INDEPENDENT or
            is_language_independent(context)
        )

        if not is_neutral_content and not INavigationRoot.providedBy(context):
            if ITranslatable.providedBy(context) and getSecurityManager().checkPermission('Manage portal', context):
                menu.append({
                    "title": _(
                        u"title_mirror_content",
                        default=u"Mirror this object to other languages"
                    ),
                    "description": _(
                        u"description_mirror_content",
                        default=u""
                    ),
                    "action": url + "/mirror_content",
                    "selected": False,
                    "icon": None,
                    "extra": {
                        "id": "_mirror_content",
                        "separator": None,
                        "class": ""
                    },
                    "submenu": None,
                })
        return menu