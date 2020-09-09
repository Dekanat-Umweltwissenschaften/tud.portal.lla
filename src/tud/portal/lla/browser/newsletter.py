from email.mime.text import MIMEText
import logging
from smtplib import SMTPException
from Products.CMFPlone.interfaces import IMailSchema

from plone.registry.interfaces import IRegistry
from plone.schema.email import Email
from plone import api
from zope.component import getUtility
from zope.interface import Interface
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form, field
from plone.z3cform.layout import wrap_form
from tud.portal.lla.interfaces import INewsletterSettings
from tud.portal.lla import _


log = logging.getLogger(__name__)


class INewsletterForm(Interface):
    """
    """
    email = Email(
        title=_('newsletter_email_address', default=u'Your email address'),
    )

class NewsletterForm(form.Form):
    """
    """
    fields = field.Fields(INewsletterForm)
    ignoreContext = True

    label = _('newsletter_form_label',
              default=u"Newsletter")
    description = _('newsletter_form_description',
                    u"Please enter your email address to (un-)subscribe to LLA-Newsletter.")

    @property
    def mailing_list_address(self):
        registry = getUtility(IRegistry)
        newsletter_settings = registry.forInterface(INewsletterSettings)
        return newsletter_settings.mailing_list_address

    @button.buttonAndHandler(_('newsletter_subscribe', default=u'Subscribe'))
    def handle_subscribe(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self.send_mail(
            message=u'subscribe address=' + data['email'],
            send_to_address=self.mailing_list_address,
        )
        IStatusMessage(self.request).addStatusMessage(_('status_message_newsletter_subscribed',
                                                        u'A request for subscribing the newsletter has been sent. Please check your emails to confirm this action.'),
                                                        'info')
        self.request.response.redirect(self.request.URL)

    @button.buttonAndHandler(_('newsletter_unsubscribe', default=u'Unsubscribe'))
    def handle_unsubscribe(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self.send_mail(
            message=u'unsubscribe address=' + data['email'],
            send_to_address=self.mailing_list_address,
        )
        IStatusMessage(self.request).addStatusMessage(_('status_message_newsletter_unsubscribed',
                                                        u'A request for unsubscribing the newsletter has been sent. Please check your emails to confirm this action.'),
                                                        'info')
        self.request.response.redirect(self.request.URL)

    def send_mail(self, message, send_to_address, subject=None):
        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        from_address = mail_settings.email_from_address
        registry = getUtility(IRegistry)
        encoding = registry.get('plone.email_charset', 'utf-8')
        host = api.portal.get_tool('MailHost')

        message = MIMEText(message, 'plain', encoding)

        try:
            # This actually sends out the mail
            host.send(
                message,
                send_to_address,
                from_address,
                subject=subject,
                charset=encoding
            )
        except (SMTPException, RuntimeError), e:
            log.error(e)
            plone_utils = api.portal.get_tool('plone_utils')
            exception = plone_utils.exceptionString()
            message = _(u'Unable to send mail: ${exception}',
                        mapping={u'exception': exception})
            IStatusMessage(self.request).add(message, type=u'error')

NewsletterView = wrap_form(NewsletterForm)

