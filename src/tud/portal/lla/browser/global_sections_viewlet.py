## @package tud.portal.lla
#  @author Paul Grunewald <paul.grunewald@tu-dresden.de>
#  @date 03.11.2016
#  @copyright TU Dresden
"""Global sections viewlet, that adds some additional sections AFTER the generated first level ones.
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import GlobalSectionsViewlet as Base
from Acquisition import aq_inner
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility

from plone import api
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlone.interfaces import INavigationSchema
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName

class GlobalSectionsViewlet(Base):
    """
    """
    index = ViewPageTemplateFile('templates/sections_viewlet.pt')

    def _selected_tab(self, portal_tabs):
        selected_tabs = self.selectedTabs(portal_tabs=portal_tabs)
        selected_portal_tab = selected_tabs['portal']
        return selected_portal_tab

    def update(self):
        super(GlobalSectionsViewlet, self).update()
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request), name='portal_tabs_view')
        context_state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        plone_tool = getToolByName(context, 'plone_utils')

        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        current_language = portal_state.language()
        translate = getToolByName(context, 'translation_service').translate

        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(
            INavigationSchema,
            prefix="plone",
            check=False
        )

        # original entries
        self.portal_tabs = portal_tabs_view.topLevelTabs()

        self.selected_portal_tab = self._selected_tab(self.portal_tabs)

        nav_root = api.portal.get_navigation_root(self)

        # get the brains of the root children objects
        root_objects = {}
        for brain in nav_root.getFolderContents():
            url = brain.getURL()
            root_objects[url] = brain

        # handle the root children objects and append their children objects
        for tab in self.portal_tabs:
            if self.selected_portal_tab == tab['id']:
                tab['selected'] = True

            if not tab['url'] in root_objects:
                continue

            tab_obj = root_objects[tab['url']].getObject()

            if not IFolderish.providedBy(tab_obj):
                continue

            if tab_obj.getLayout() == 'full_view':
                continue

            if tab_obj.getLayout() == 'event_listing':
                status = api.content.get_state(obj=tab_obj)
                tab['children'] = [{
                    'name': translate("mode_past_link", domain="plone.app.event", target_language=current_language, default="Past"),
                    'id': tab_obj.getId() + "_past_events",
                    'url': tab_obj.absolute_url() + "/event_listing?mode=past",
                    'review_state': status
                }]
                continue

            children = tab_obj.getFolderContents()
            children = [child.getObject() for child in children]
            result = []
            for child in children:
                if plone_tool.isDefaultPage(child):
                    continue

                if hasattr(child, "getExcludeFromNav") and child.getExcludeFromNav():
                    continue

                if child.portal_type not in navigation_settings.displayed_types:
                    continue

                status = api.content.get_state(obj=child)
                data = {
                    'name': utils.pretty_title_or_id(context, child),
                    'id': child.getId(),
                    'url': child.absolute_url(),
                    'description': child.Description(),
                    'review_state': status
                }
                result.append(data)

            tab['children'] = result


        # append foots_actions to the menu
        footer_actions = context_state.actions('footer_actions')
        self.extra_tabs = []

        # Appended entries
        for actionInfo in footer_actions:
            data = actionInfo.copy()
            data['name'] = data['title']
            self.extra_tabs.append(data)

        self.selected_extra_tab = self._selected_tab(self.extra_tabs)
