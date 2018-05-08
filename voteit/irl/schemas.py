import colander
import deform
from arche.validators import existing_userid_or_email
from six import string_types
from voteit.core import security
from voteit.core.helpers import strip_and_truncate
from voteit.core.schemas.common import deferred_autocompleting_userid_widget
from voteit.core.schemas.common import HASHTAG_PATTERN
from voteit.core.schemas.common import strip_and_lowercase
from voteit.irl import _
from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.models.interfaces import IElegibleVotersMethod
from voteit.irl.models.interfaces import IParticipantNumbers


@colander.deferred
def elegible_voters_method_choices_widget(node, kw):
    """ Create a widget where you can choose all selectable methods to adjust elegible voters. """
    context = kw['context']
    request = kw['request']
    method_choices = [('', _('<Select>'))]
    for (name, method) in request.registry.getAdapters([context], IElegibleVotersMethod):
        method_choices.append((name, method.title))
    return deform.widget.SelectWidget(values=method_choices)


class ElegibleVotersMethodSchema(colander.Schema):
    method_name = colander.SchemaNode(
        colander.String(),
        title=_(u"elegible_voters_method_name",
                default=u"Method to select elegible voters"),
        description=_(u"elegible_voters_method_description",
                      default=u"It will modify the voting permissions "
                              u"accoring to it's specifications."),
        widget=elegible_voters_method_choices_widget,
    )


@colander.deferred
def register_diff_choices_widget(node, kw):
    context = kw['context']
    request = kw['request']
    electoral_register = request.registry.getAdapter(context, IElectoralRegister)
    choices = []
    for id in sorted(electoral_register.registers.keys(), key=int, reverse=True):
        timestamp = request.dt_handler.format_dt(electoral_register.registers[id]['time'])
        title = "%s: %s" % (id, timestamp)
        choices.append((id, title))
    return deform.widget.SelectWidget(values=choices)


class ElectoralRegisterDiffSchema(colander.Schema):
    first = colander.SchemaNode(
        colander.Int(),
        title=_(u"First register"),
        widget=register_diff_choices_widget,
    )
    second = colander.SchemaNode(
        colander.Int(),
        title=_(u"Second register"),
        widget=register_diff_choices_widget,
    )


@colander.deferred
def deferred_participant_number_token_validator(node, kw):
    context = kw['context']
    request = kw['request']
    return PNTokenValidator(context, request)


class PNTokenValidator(object):
    """ For meetings """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, node, value):
        participant_numbers = self.request.registry.getAdapter(self.context, IParticipantNumbers)
        if value not in participant_numbers.token_to_number:
            raise colander.Invalid(node, _(u"No match - remember that it's case sensitive!"))
        number = participant_numbers.token_to_number[value]
        if participant_numbers.tickets[number].claimed:
            raise colander.Invalid(node, _(u"This number has already been claimed."))


class ClaimParticipantNumberSchema(colander.Schema):
    token = colander.SchemaNode(
        colander.String(),
        validator=deferred_participant_number_token_validator,
        title=_("Access code for participant number"),
        description=_(u"enter_token_description",
                      default=u"Enter the code sent to you. It will have "
                              u"the format xxxx-xxxx. "
                              u"Note that it's case sensitive and can only be used once.")
    )


@colander.deferred
def deferred_existing_participant_number_validator(node, kw):
    request = kw['request']
    context = request.meeting
    return ExistingParticipantNumberValidator(context, request)


class ExistingParticipantNumberValidator(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, node, value):
        pn = self.request.registry.getAdapter(self.context, IParticipantNumbers)
        if value not in pn.number_to_userid.keys():
            return colander.Invalid(node, _(u"Participant number not found"))


@colander.deferred
def emails_matches_start_and_existing_nums(form, kw):
    return EmailsMatchesStartAndExistingNumbersValidator(kw['context'], kw['request'])


class EmailsMatchesStartAndExistingNumbersValidator(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, form, values):
        exc = colander.Invalid(form)  # Raised if trouble
        pns = self.request.registry.getAdapter(self.request.meeting, IParticipantNumbers)
        numbers = tuple(pns.tickets.keys())
        start_at = values['start_at']
        if start_at not in numbers and not values['create_new']:
            exc['start_at'] = _("Not an existing participant number")
            raise exc
        existing_emails = tuple([x.email for x in pns.tickets.values()])
        found = []
        i = start_at
        emails = values['emails'].splitlines()
        for email in emails:
            if email in existing_emails:
                found.append(email)
            if not values['create_new']:
                # Check if numbers exist
                if i not in numbers:
                    exc['emails'] = _("attach_emails_pn_dont_exist_error",
                                      default="There are more email addresses than "
                                              "existing participant numbers. "
                                              "Number ${num} not found. Total emails: ${emails_count}",
                                      mapping={'num': i, 'emails_count': len(emails)})
                    raise exc
                i += 1
        if found:
            exc['emails'] = _("The following emails are already assigned to numbers: ${emails}",
                              mapping={'emails': ", ".join(found)})
            raise exc


def multiple_email_w_whitespace_validator(node, value):
    """ Checks that each line of value is a correct email. Skips whitespace.
    """
    validator = colander.Email()
    invalid = []
    for email in value.splitlines():
        if not email:
            continue
        try:
            validator(node, email)
        except colander.Invalid:
            invalid.append(email)
    if invalid:
        emails = ", ".join(invalid)
        raise colander.Invalid(node, _(u"The following adresses is invalid: ${emails}",
                                       mapping={'emails': emails}))


class AttachEmailsToPN(colander.Schema):
    title = _("Attach emails")
    start_at = colander.SchemaNode(colander.Int(),
                                   title=_("Start at number"))
    validator = emails_matches_start_and_existing_nums
    emails = colander.SchemaNode(
        colander.String(),
        title=_("add_tickets_emails_titles",
                default="Email addresses to attach."),
        description=_("attach_emails_description",
                      default="Paste a list of email addresses, "
                              "one per row, to attach to participant numbers. "
                              "They will be attached in sequence starting at the specified start number. "
                              "If any of them exist as validated users, the participant numbers will be "
                              "assigned to them. If not, numbers will automatically be assigned when an "
                              "email address is validated. Empty lines will "
                              "increase number but has no other effect."),
        widget=deform.widget.TextAreaWidget(rows=7, cols=40),
        preparer=strip_and_lowercase,
        validator=multiple_email_w_whitespace_validator,
    )
    create_new = colander.SchemaNode(
        colander.Bool(),
        title=_("Create new tickets if they don't exist"),
        default=True,
        missing=False
    )


def _meeting_roles_minus_moderator():
    roles = dict(security.MEETING_ROLES)
    del roles[security.ROLE_MODERATOR]
    return roles.items()


class ConfigureParticipantNumberAP(colander.Schema):
    pn_ap_claimed_roles = colander.SchemaNode(
        colander.Set(),
        title=_(u"Anyone registering with participant number will be given these roles"),
        description=_(u"pn_ap_claimed_roles_description",
                      default=u"Picking at least one is required. "
                              u"Note that if you allow registration to be "
                              u"bypassed (see below) the roles "
                              u"specified here won't be added when a meeting number is "
                              u"claimed by someone who's already a part of the meeting."),
        default=[security.ROLE_VIEWER],
        widget=deform.widget.CheckboxChoiceWidget(values=_meeting_roles_minus_moderator()),
    )
    pn_ap_public_roles = colander.SchemaNode(
        colander.Set(),
        title=_(u"Allow bypass and give access to anyone?"),
        description=_(u"pn_ap_public_roles_description",
                      default=u"If anything is checked below, any user will be able to bypass the access form "
                              u"and immediately gain the roles checked. Some examples - for meetings that are: \n\n"
                              u"Closed: check nothing below.\n"
                              u"Viewable for anyone: check view permission\n"
                              u"Open for participation from anyone: check all\n"),
        widget=deform.widget.CheckboxChoiceWidget(values=_meeting_roles_minus_moderator()),
    )


@colander.deferred
def deferred_autocompleting_participant_number_widget(node, kw):
    request = kw['request']
    meeting = request.meeting
    pn = request.registry.getAdapter(meeting, IParticipantNumbers)
    choices = tuple(pn.number_to_userid.keys())
    return deform.widget.AutocompleteInputWidget(
        size=15,
        values=choices,
        min_length=1)


@colander.deferred
def deferred_pn_from_get(node, kw):
    request = kw['request']
    val = request.GET.get('pn', colander.null)
    if isinstance(val, string_types):
        try:
            return int(val)
        except:
            pass
    return colander.null


class AssignParticipantNumber(colander.Schema):
    title = _("Assign participant number")
    userid = colander.SchemaNode(
        colander.String(),
        title=_(u"UserID"),
        validator=existing_userid_or_email,
        widget=deferred_autocompleting_userid_widget,
    )
    pn = colander.SchemaNode(
        colander.Int(),
        widget=deform.widget.HiddenWidget(),
        default=deferred_pn_from_get,
    )


def add_proposals_owner_nodes(schema, proposals):
    for obj in proposals:
        name = obj.__name__
        title = obj.get_field_value('aid')
        description = strip_and_truncate(obj.title, limit=150)
        schema.add(
            colander.SchemaNode(
                colander.String(),
                name=name,
                title=title,
                description=description,
                validator=existing_userid_or_email,
                widget=deferred_autocompleting_userid_widget
            )
        )


def add_discussions_owner_nodes(schema, discussion_posts):
    for obj in discussion_posts:
        name = obj.__name__
        title = name
        description = strip_and_truncate(obj.title, limit=150)
        schema.add(
            colander.SchemaNode(
                colander.String(),
                name=name,
                title=title,
                description=description,
                validator=existing_userid_or_email,
                widget=deferred_autocompleting_userid_widget,
            )
        )


class MeetingPresenceSettingsSchema(colander.Schema):
    enabled = colander.SchemaNode(
        colander.Bool(),
        title = _("Make meeting presence check available?"),
    )


class MainProposalsSettingsSchema(colander.Schema):
    main_proposal_hashtag_name = colander.SchemaNode(
        colander.String(),
        title=_('Main proposal hashtag'),
        description=_('Set to hashtag name (without #) to enable main proposals.'),
        missing='',
        validator=colander.Regex(
            HASHTAG_PATTERN,
            msg=_('Invalid hashtag format. (Use only a-Z,1-9,_,-)')
        ),
    )


def includeme(config):
    config.add_content_schema('Meeting', ElegibleVotersMethodSchema, 'eligible_voters_method')
    config.add_content_schema('Meeting', AssignParticipantNumber, 'assign_participant_number')
    config.add_content_schema('Meeting', ClaimParticipantNumberSchema, 'claim_participant_number')
    config.add_content_schema('Meeting', AttachEmailsToPN, 'attach_emails_to_pn')
    config.add_content_schema('Meeting', MeetingPresenceSettingsSchema, 'meeting_presence_settings')
    config.add_content_schema('Meeting', MainProposalsSettingsSchema, 'main_proposals_settings')
