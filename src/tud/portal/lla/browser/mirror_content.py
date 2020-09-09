## @package tud.portal.lla
#  @author Paul Grunewald <paul.grunewald@tu-dresden.de>
#  @date 12.12.2016
#  @copyright TU Dresden
"""Form to mirror content from place within a language folder to a different one.
"""
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.interfaces import IFolderish
from plone import api
from plone.app.z3cform.utils import closest_content
from zope.interface import Interface, directlyProvides
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form, field
from zope.schema import Choice, List, Bool
from plone.z3cform.layout import wrap_form
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.multilingual.interfaces import ITranslationManager, ITranslatable

from tud.portal.lla import _

def recursively_bind_translation(source, target, language, keep_workflow_states):

    if ITranslatable.providedBy(source):
        tm_source = ITranslationManager(source)
        tm_source.register_translation(language=language, content=target)

    if keep_workflow_states:
        try:
            api.content.transition(target, to_state=api.content.get_state(source))
        except WorkflowException:
            pass

    if IFolderish.providedBy(source) and IFolderish.providedBy(target):
        for source_obj_id, source_obj in source.objectItems():
            target_obj = target[source_obj_id]
            recursively_bind_translation(source_obj, target_obj, language, keep_workflow_states)

## @brief Provider for all available languages.
#  @param context current context
#  @returns SimpleVocabulary
def available_languages_provider(context):
    """
    Create a vocabulary with all available languages
    """
    # fail-safe context
    context = closest_content(context)

    ltool = api.portal.get_tool('portal_languages')
    supported_languages = ltool.getSupportedLanguages()
    tm = ITranslationManager(context)
    translated_languages = tm.get_translated_languages()

    items = [(l, info.get('name', l)) for (l, info) in ltool.getAvailableLanguageInformation().items() if l in supported_languages and l not in translated_languages]
    items = [SimpleTerm(i[0], i[0], i[1]) for i in items]

    return SimpleVocabulary(items)
directlyProvides(available_languages_provider, IContextSourceBinder)


## @brief Form data
class IMirrorContent(Interface):
    """
    """

    languages = List(
        title=_(u'Languages'),
        description=_(u'Choose the languages you wish to translate this content object.'),
        value_type=Choice(source=available_languages_provider),
        required=True,
        missing_value=[])

    keep_workflow_states = Bool(
        title=_(u'Keep workflow states?'),
        description=_(u'If checked, copied contents will also have the same state of the original content. Otherwise, it will be in the initial state (e.g. private).'),
        default=True,
    )

## @brief Our form
class MirrorContentForm(form.Form):
    """Form to mirror content from place within a language folder to a different one.
    """
    fields = field.Fields(IMirrorContent)
    ignoreContext = True

    label = _('mirror_content_form_label',
              default=u"Mirror this object to other languages.")
    description = _('mirror_content_form_description',
                    u"With this form you can replicate the current object and its children from this language folder into another language folders. You still have to make sure, that the container path is present in the destination location.")

    output = None

    submitted = False

    @property
    def already_translated(self):
        tm = ITranslationManager(self.context)
        return tm.get_translations()

    ## @brief Definition of the button and handler for removing protection
    @button.buttonAndHandler(_('button_mirror_content', default=u'Mirror content'))
    def handle_mirror_content(self, action):
        self.submitted = True

        data, errors = self.extractData()
        if errors:
            return False

        languages = data['languages']
        keep_workflow_states = data['keep_workflow_states']

        self.output = None
        context = self.context
        portal = api.portal.get()

        # Relative from LRF object
        relative_path = context.getPhysicalPath()[len(portal.getPhysicalPath())+1:]

        # Check precondition
        for l in languages:
            l = str(l)
            # Check for container
            container_path = '/'.join((l,) + relative_path[:-1])
            if portal.unrestrictedTraverse(container_path, default=None) is None:

                IStatusMessage(self.request).addStatusMessage(_('status_mirror_content_not_found',
                                                                u'Did not find container ${path}.',
                                                                mapping={'path': container_path}),
                                                                'warning')
                return False

        # Copy and bind
        for l in languages:
            l = str(l)
            container_path = '/'.join((l,) + relative_path[:-1])
            container = portal.unrestrictedTraverse(container_path)
            target = api.content.copy(self.context, container)
            recursively_bind_translation(self.context, target, l, keep_workflow_states)

        IStatusMessage(self.request).addStatusMessage(_('status_mirror_content_success',
                                                        u'Contents successfully mirrored for ${languages}.',
                                                        mapping={'languages': ', '.join(languages)}),
                                                        'info')

        redirect_url = "%s/@@%s" % (self.context.absolute_url(), self.__name__)
        self.request.response.redirect(redirect_url)


## @brief Wrapper (including a custom template to show protection information)
MirrorContentFormView = wrap_form(MirrorContentForm,
                              index=FiveViewPageTemplateFile("templates/mirror_content.pt"))

