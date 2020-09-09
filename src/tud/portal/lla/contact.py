from plone.supermodel import model


class IContact(model.Schema):

    """Schema for contact content type."""

    model.load('models/contact.xml')