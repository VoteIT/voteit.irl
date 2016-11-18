from arche.views.base import BaseView
from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.view import view_config
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUser

from voteit.irl import _
from voteit.irl.models.interfaces import IParticipantNumbers


class ParticipantNumbersView(BaseView):

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.context, IParticipantNumbers)

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
class AttachEmailsToPNForm(DefaultEditForm):
    schema_name = 'attach_emails_to_pn'

    @property
    def title(self): #<- This will probably change in arche
        return self.schema.title

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.context, IParticipantNumbers)

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
        for email in emails:
            self.participant_numbers.attach_email(email, i)
            user = users.get_user_by_email(email, only_validated = True)
            if user:
                ticket = self.participant_numbers.tickets[i]
                self.participant_numbers.claim_ticket(user.userid, ticket.token)
                auto_claimed += 1
            i += 1
        msg = _("<b>${emails_num}</b> attached.",
                mapping = {'emails_num': len(emails)})
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
class ClaimParticipantNumberForm(DefaultEditForm):
    """ This view is for participants who're already members of this meeting,
        but haven't registered their number yet.
    """
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

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.context, IParticipantNumbers)

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
class AssignParticipantNumberForm(DefaultEditForm):
    schema_name = 'assign_participant_number'

    @property
    def title(self):
        return self.schema.title

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.context, IParticipantNumbers)

    def appstruct(self):
        appstruct = {}
        pn = int(self.request.GET['pn'])
        appstruct['userid'] = self.participant_numbers.number_to_userid.get(pn, "")
        return appstruct

    def save_success(self, appstruct):
        #Since this is a bit backwards, we need to fetch the token.
        pn = appstruct['pn']
        userid = appstruct['userid']
        found = False
        for (token, num) in self.participant_numbers.token_to_number.items():
            if num == pn:
                found = True
                break
        if not found:
            raise HTTPForbidden(_(u"Participant number not found"))
        #Clear old number?
        if userid in self.participant_numbers.userid_to_number:
            number = self.participant_numbers.userid_to_number[userid]
            msg = _("participant_number_moved_warning",
                    default = u"This user was already assigned number ${number} so that number was cleared.",
                    mapping = {'number': number})
            self.flash_messages.add(msg, type = 'warning')
            self.participant_numbers.clear_number(number)
        #Assign
        number = self.participant_numbers.claim_ticket(userid, token)
        msg = _("number_now_assigned_notice",
                default = "You're now assigned number ${number}.",
                mapping = {'number': number})
        self.flash_messages.add(msg)
        return HTTPFound(location = self.request.resource_url(self.context, "manage_participant_numbers"))


@view_action('settings_menu', 'participant_numbers',
             permission = security.MODERATE_MEETING)
def participant_numbers_menu(context, request, va, **kw):
    return """<li><a href="%s">%s</a></li>""" % (request.resource_url(request.meeting, "manage_participant_numbers"),
                                                 request.localizer.translate(_("Manage participant numbers")))

@view_action('participants_menu', 'claim_participant_number',
             permission = security.VIEW)
def claim_participant_number_menu(context, request, va, **kw):
    if request.meeting:
        participant_numbers = request.registry.getAdapter(request.meeting, IParticipantNumbers)
        if request.authenticated_userid not in participant_numbers.userid_to_number:
            return """<li><a href="%s">%s</a></li>""" % (request.resource_url(request.meeting, 'claim_participant_number'),
                                                         request.localizer.translate(_("Claim participant number")))
        else:
            return """<li class="disabled"><a>%s: %s</a></li>""" % (
                request.localizer.translate(_("Your participant number")),
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
