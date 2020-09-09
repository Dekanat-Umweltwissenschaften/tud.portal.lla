from plone.app.registry.browser import controlpanel
from tud.portal.lla.interfaces import INewsletterSettings
from tud.portal.lla import _

class NewsletterControlPanelForm(controlpanel.RegistryEditForm):
    """
    """
    schema = INewsletterSettings
    label = _('control_panel_newsletter_label', default=u'Newsletter')
    description = _('control_panel_newsletter_desc', default=u'Newsletter-relevant settings.')

class NewsletterControlPanel(controlpanel.ControlPanelFormWrapper):
    """
    """
    form = NewsletterControlPanelForm
