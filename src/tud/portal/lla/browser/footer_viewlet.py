## @package tud.portal.lla
#  @author Paul Grunewald <paul.grunewald@tu-dresden.de>
#  @date 02.11.2016
#  @copyright TU Dresden
"""A footer viewlet
"""

from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter


class FooterViewlet(ViewletBase):
    """
    """

    ## @brief Overridden PersonalBarViewlet's method
    #  @return None
    def update(self):
        # Add system actions
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        footer_actions = context_state.actions('footer_actions')

        self.footer_actions = []

        for action in footer_actions:
            info = {
                'title': action['title'],
                'href': action['url'],
                'id': 'personaltools-{}'.format(action['id']),
                'target': 'link_target' in action and action['link_target'] or None,
                }
            modal = action.get('modal')
            if modal:
                info['class'] = 'pat-plone-modal'
                info['data-pat-plone-modal'] = modal
            self.footer_actions.append(info)

