# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope import schema
from zope.interface import Interface

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from tud.portal.lla import _


class ITudPortalLlaLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IImprintPage(Interface):
    """Marker Interface to indicate, that the content is an imprint page.
    """

class IAccessibilityDeclarationPage(Interface):
    """Marker Interface to indicate, that the content is the accessibility declaration page.
    """

class INewsletterSettings(Interface):
    """Settings for newsletter.
    """

    mailing_list_address = schema.TextLine(
        title=_("mailing_list_address", default=u"Mailing list address"),
        description=_("mailing_list_address_description", default=u"When the mailing list address is mylist@groups.tu-dresden.de, this entry should be mylist-request@groups.tu-dresden.de. This only works for mailman as system."),
        default=None,
        required=True
    )
