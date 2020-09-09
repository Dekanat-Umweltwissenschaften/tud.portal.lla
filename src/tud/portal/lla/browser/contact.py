from Products.CMFPlone.browser.contact_info import ContactForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ContactView(ContactForm):

    template = ViewPageTemplateFile('templates/contact.pt')

    @property
    def introduction_text(self):
        return self.context.text

    @property
    def email(self):
        return self.context.email

    @property
    def phone(self):
        return self.context.phone

    @property
    def address(self):
        return self.context.address
