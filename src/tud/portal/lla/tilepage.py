from tud.portal.lla import MessageFactory as _
from plone.supermodel import model
from zope import schema

class ITilePage(model.Schema):

    """Schema for Conference Presenter content type."""

    model.load('models/tilePage.xml')