from arche.views.base import BaseView, BaseForm
from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from deform import Button
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.view import view_config
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUser
from voteit.core.views.control_panel import control_panel_category
from voteit.core.views.control_panel import control_panel_link
from voteit.core import security

from voteit.irl import _
from voteit.irl.models.interfaces import IParticipantNumbers
from voteit.irl.models.interfaces import ISelfAssignmentSettings
from voteit.irl.models.participant_numbers import assign_next_free_pn


class PNViewMixin(object):

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.context, IParticipantNumbers)

    @reify
    def self_assignment_settings(self):
        return self.request.registry.getAdapter(self.context, ISelfAssignmentSettings)


class ParticipantNumbersView(BaseView, PNViewMixin):

    @view_config(name = "manage_participant_numbers",
                 permission = security.MODERATE_MEETING,
                 context = IMeeting,
                 renderer = "voteit.irl:templates/participant_numbers.pt")
    def manage_participant_numbers(self):
        if 'back' in self.request.POST:
            return HTTPFound(location = self.request.resource_url(self.context))
        response = {}
        add = 'add' in self.request.POST
        remove = 'remove' in self.request.POST
        here_url = self.request.resource_url(self.context, 'manage_participant_numbers')
        if add or remove:
            #Basic validation
            try:
                start = self.request.POST.get('start', None)
                start = int(start)
                end = self.request.POST.get('end', None)
                if not end:
                    end = None
                else:
                    end = int(end)
                    if start > end:
                        raise HTTPForbidden(_(u"End must be higher than start"))
            except TypeError:
                raise HTTPForbidden(_(u"Must be an integer value"))
            if add:
                res = self.participant_numbers.new_tickets(self.request.authenticated_userid, start, end)
                msg = _(u"Added ${count} new numbers",
                        mapping = {'count': len(res)})
                self.flash_messages.add(msg)
            if remove:
                res = self.participant_numbers.clear_numbers(start, end)
                msg = _(u"Removed ${count} numbers",
                        mapping = {'count': len(res)})
                self.flash_messages.add(msg, type = "warning")
            return HTTPFound(location = here_url)
        response['participant_numbers'] = self.participant_numbers
        return response


@view_config(name = "attach_emails_to_pn",
             permission = security.MODERATE_MEETING,
             renderer = "arche:templates/form.pt")
class AttachEmailsToPNForm(DefaultEditForm, PNViewMixin):
    schema_name = 'attach_emails_to_pn'

    @property
    def title(self):
        return self.schema.title

    def cancel_success(self, *args):
        return HTTPFound(location = self.request.resource_url(self.context, 'manage_participant_numbers'))

    def save_success(self, appstruct):
        emails = appstruct['emails'].splitlines()
        start_at = appstruct['start_at']
        create_new = appstruct['create_new']
        #First, create new tickets if ordered to
        messages = []
        translate = self.request.localizer.translate
        if create_new:
            end_at = start_at + len(emails) - 1
            res = self.participant_numbers.new_tickets(self.request.authenticated_userid, start_at, end_at)
            if res:
                msg = _(u"<b>${count}</b> new participant numbers created.",
                        mapping = {'count': len(res)})
                messages.append(translate(msg))
        i = start_at
        users = self.root['users']
        auto_claimed = 0
        empty = 0
        for email in emails:
            if not email:
                i += 1
                empty += 1
                continue
            self.participant_numbers.attach_email(email, i)
            user = users.get_user_by_email(email, only_validated = True)
            if user:
                ticket = self.participant_numbers.tickets[i]
                self.participant_numbers.claim_ticket(user.userid, ticket.token)
                auto_claimed += 1
            i += 1
        msg = _("<b>${emails_num}</b> attached.",
                mapping = {'emails_num': len(emails)-empty})
        messages.append(translate(msg))
        if auto_claimed:
            msg = _("<b>${num}</b> numbers were auto-claimed by users with validated email addresses.",
                    mapping = {'num': auto_claimed})
            messages.append(translate(msg))
        self.flash_messages.add(" ".join(messages), auto_destruct = False)
        return HTTPFound(location = self.request.resource_url(self.context, 'manage_participant_numbers'))


@view_config(name = "claim_participant_number",
             permission = security.VIEW,
             renderer = "arche:templates/form.pt")
class ClaimParticipantNumberForm(DefaultEditForm, PNViewMixin):
    """ This view is for participants who're already members of this meeting,
        but haven't registered their number yet.
    """
    title = _("Claim participant number")
    schema_name = 'claim_participant_number'

    def __call__(self):
        userid = self.request.authenticated_userid
        if userid in self.participant_numbers.userid_to_number:
            number = self.participant_numbers.userid_to_number[userid]
            msg = _(u"already_assigned_number_error",
                    default = u"You've already been assigned the number ${number} so you don't need to do anything else.",
                    mapping = {'number': number})
            self.flash_messages.add(msg, type = 'warning')
            return HTTPFound(location = self.request.resource_url(self.context))
        return super(ClaimParticipantNumberForm, self).__call__()

    def save_success(self, appstruct):
        number = self.participant_numbers.claim_ticket(self.request.authenticated_userid, appstruct['token'])
        msg = _("number_now_assigned_notice",
                default = "You're now assigned number ${number}.",
                mapping = {'number': number})
        self.flash_messages.add(msg)
        return HTTPFound(location = self.request.resource_url(self.context))


@view_config(name = "assign_participant_number",
             permission = security.MODERATE_MEETING,
             renderer = "arche:templates/form.pt")
class AssignParticipantNumberForm(DefaultEditForm, PNViewMixin):
    schema_name = 'assign_participant_number'

    @property
    def title(self):
        return self.schema.title

    def appstruct(self):
        appstruct = {}
        pn = int(self.request.GET['pn'])
        appstruct['userid'] = self.participant_numbers.number_to_userid.get(pn, "")
        return appstruct

    def save_success(self, appstruct):
        # Since this is a bit backwards, we need to fetch the token.
        pn = appstruct['pn']
        userid = appstruct['userid']
        found = False
        for (token, num) in self.participant_numbers.token_to_number.items():
            if num == pn:
                found = True
                break
        if not found:
            raise HTTPForbidden(_(u"Participant number not found"))
        # Clear old number?
        if userid in self.participant_numbers.userid_to_number:
            number = self.participant_numbers.userid_to_number[userid]
            msg = _("participant_number_moved_warning",
                    default = u"This user was already assigned number ${number} so that number was cleared.",
                    mapping = {'number': number})
            self.flash_messages.add(msg, type = 'warning')
            self.participant_numbers.clear_number(number)
        # Assign
        number = self.participant_numbers.claim_ticket(userid, token)
        msg = _("number_now_assigned_notice",
                default = "You're now assigned number ${number}.",
                mapping = {'number': number})
        self.flash_messages.add(msg)
        return HTTPFound(location = self.request.resource_url(self.context, "manage_participant_numbers"))


@view_config(name = "pn_self_assignment_settings",
             permission = security.MODERATE_MEETING,
             renderer = "arche:templates/form.pt")
class PNSelfAssignmentSettingsForm(DefaultEditForm, PNViewMixin):
    schema_name = 'self_assignment_settings'
    title = _("Self assignment settings")
    description = _("Allow participants to assign a number to themselves?")

    def appstruct(self):
        return dict(self.self_assignment_settings)

    def save_success(self, appstruct):
        self.self_assignment_settings.update(appstruct)
        self.flash_messages.add(self.default_success, type='success')
        return HTTPFound(location = self.request.resource_url(self.context, "manage_participant_numbers"))


@view_config(name = "self_claim_participant_number",
             permission = security.VIEW,
             renderer = "arche:templates/form.pt")
class PNSelfClaimForm(DefaultEditForm, PNViewMixin):
    schema_name = 'self_claim_participant_number'

    @property
    def title(self):
        return self.schema.title

    @property
    def buttons(self):
        return (Button('assign', _("Assign")), self.button_cancel)

    def assign_success(self, appstruct):
        start_number = self.self_assignment_settings.get('start_number', None)
        if not isinstance(start_number, int):
            self.flash_messages.add(_("Meeting has bad configurartion for participant numbers, contact the moderator.",
                                      type='danger'))
            return HTTPFound(location=self.request.resource_url(self.context))
        new_pn = assign_next_free_pn(self.participant_numbers, self.request.authenticated_userid, start_number)
        if not new_pn:
            raise HTTPBadRequest("No number can be assigned.")
        msg = _("You've been assigned number ${num}", mapping={'num': new_pn})
        self.flash_messages.add(msg, type='success')
        return HTTPFound(location = self.request.resource_url(self.context))


@view_action('user_menu', 'claim_participant_number',
             permission = security.VIEW, priority=20)
def claim_participant_number_menu(context, request, va, **kw):
    if request.meeting:
        translate = request.localizer.translate
        participant_numbers = request.registry.getAdapter(request.meeting, IParticipantNumbers)
        if request.authenticated_userid not in participant_numbers.userid_to_number:
            self_assignment = request.registry.getAdapter(request.meeting, ISelfAssignmentSettings)
            if self_assignment.enabled:
                if self_assignment.user_has_required_role(request):
                    url = request.resource_url(request.meeting, 'self_claim_participant_number')
                else:
                    # The current user don't have the required role
                    role = request.registry.roles.get(self_assignment.required_role, None)
                    if role:
                        role_title = translate(role.title)
                    else:
                        role_title = self_assignment.required_role
                    return """<li class="disabled"><a>%s<br/>%s</a></li>""" % (
                           translate(
                               _("You lack the role '${role}'",
                                 mapping={'role': role_title})
                           ),
                           translate(
                               _("which is required to request a participant number.")
                           ),
                    )

            else:
                url = request.resource_url(request.meeting, 'claim_participant_number')
            return """<li><a href="%s">%s</a></li>""" % (url,
                                                         translate(_("Claim participant number")))
        else:
            return """<li class="disabled"><a>%s: %s</a></li>""" % (
                translate(_("Your participant number")),
                participant_numbers.userid_to_number[request.authenticated_userid]
            )


@view_action('user_info', 'participant_number',
             interface = IUser)
def participant_number_info(context, request, va, **kw):
    if not request.meeting:
        return
    participant_numbers = request.registry.getAdapter(request.meeting, IParticipantNumbers)
    if context.userid in participant_numbers.userid_to_number:
        response = dict(
            number = participant_numbers.userid_to_number[context.userid],
            context = context)
        return render("voteit.irl:templates/user_participant_number_info.pt", response, request = request)


def pn_active(context, request, va):
    participant_numbers = request.registry.queryAdapter(request.meeting, IParticipantNumbers)
    if participant_numbers:
        return bool(len(participant_numbers))
    return False


def includeme(config):
    config.scan(__name__)
    config.add_view_action(
        control_panel_category,
        'control_panel', 'pn',
        panel_group = 'control_panel_pn',
        title=_("Participant numbers"),
        description=_("Needed for physical meetings and speaker lists"),
        permission = security.MODERATE_MEETING,
        check_active=pn_active
    )
    config.add_view_action(
        control_panel_link,
        'control_panel_pn', 'participant_numbers',
        title=_("Manage participant numbers"),
        view_name='manage_participant_numbers',
    )
    config.add_view_action(
        control_panel_link,
        'control_panel_pn', 'self_assignment_settings',
        title=_("User self-assignment"),
        view_name='pn_self_assignment_settings',
    )
