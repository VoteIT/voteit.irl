import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.decorator import reify
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from betahaus.pyracont.factories import createSchema
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IUser
from voteit.core.views.base_view import BaseView

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IParticipantNumbers


class ParticipantNumbersView(BaseView):

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.api.meeting, IParticipantNumbers)

    @view_config(name = "manage_participant_numbers", context = IMeeting, permission = security.MODERATE_MEETING,
                 renderer = "templates/participant_numbers.pt")
    def manage_participant_numbers(self):
        if 'back' in self.request.POST:
            return HTTPFound(location = self.api.meeting_url)
        add = 'add' in self.request.POST
        remove = 'remove' in self.request.POST
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
                res = self.participant_numbers.new_tickets(self.api.userid, start, end)
                msg = _(u"Added ${count} new numbers",
                        mapping = {'count': len(res)})
            if remove:
                res = self.participant_numbers.clear_numbers(start, end)
                msg = _(u"Removed ${count} numbers",
                        mapping = {'count': len(res)})
            self.api.flash_messages.add(msg)
            here_url = self.request.resource_url(self.context, 'manage_participant_numbers')
            return HTTPFound(location = here_url)
        self.response['participant_numbers'] = self.participant_numbers
        return self.response

    @view_config(name = "claim_participant_number", context = IMeeting, permission = security.VIEW,
                 renderer = "voteit.core.views:templates/base_edit.pt")
    def claim_participant_number(self):
        """ This view is for participants who're already members of this meeting,
            but haven't registered their number yet.
        """
        if self.api.userid in self.participant_numbers.userid_to_number:
            number = self.participant_numbers.userid_to_number[self.api.userid]
            msg = _(u"already_assigned_number_error",
                    default = u"You've already been assigned the number ${number} so you don't need to do anything else.",
                    mapping = {'number': number})
            self.api.flash_messages.add(msg, type = 'error')
            return HTTPFound(location = self.api.meeting_url)
        schema = createSchema('ClaimParticipantNumber')
        schema = schema.bind(context = self.context, request  = self.request, api = self.api)
        form = deform.Form(schema, buttons = [deform.Button('submit', title = _(u"Submit"))])
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            number = self.participant_numbers.claim_ticket(self.api.userid, appstruct['token'])
            msg = _(u"number_now_assigned_notice",
                    default = u"You're now assigned number ${number}.",
                    mapping = {'number': number})
            self.api.flash_messages.add(msg)
            return HTTPFound(location = self.api.meeting_url)
        self.response['form'] = form.render()
        return self.response

    @view_config(name = "assign_participant_number", context = IMeeting, permission = security.MODERATE_MEETING,
                 renderer = "voteit.core.views:templates/base_edit.pt")
    def assign_participant_number(self):
        schema = createSchema('AssignParticipantNumber')
        schema = schema.bind(context = self.context, request  = self.request, api = self.api)
        form = deform.Form(schema, buttons = [deform.Button('submit', title = _(u"Submit"))])
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
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
                msg = _(u"participant_number_moved_warning",
                        default = u"This user was already assigned number ${number} so that number was cleared.",
                        mapping = {'number': number})
                self.api.flash_messages.add(msg)
                self.participant_numbers.clear_number(number)
            #Assign
            number = self.participant_numbers.claim_ticket(userid, token)
            msg = _(u"number_now_assigned_notice",
                    default = u"You're now assigned number ${number}.",
                    mapping = {'number': number})
            self.api.flash_messages.add(msg)
            return HTTPFound(location = self.request.resource_url(self.context, "manage_participant_numbers"))
        appstruct = {}
        pn = int(self.request.GET['pn'])
        appstruct['userid'] = self.participant_numbers.number_to_userid.get(pn, u"")
        self.response['form'] = form.render(appstruct = appstruct)
        return self.response


@view_action('meeting', 'participant_numbers', permission = security.MODERATE_MEETING)
def participant_numbers_menu(context, request, va, **kw):
    api = kw['api']
    return """<li><a href="%s">%s</a></li>""" % ("%smanage_participant_numbers" % api.meeting_url,
                                                 api.translate(_(u"Participant numbers")))

@view_action('meeting', 'claim_participant_number', permission = security.VIEW)
def claim_participant_number_menu(context, request, va, **kw):
    api = kw['api']
    if not api.meeting:
        return u""
    participant_numbers = request.registry.getAdapter(api.meeting, IParticipantNumbers)
    if api.userid in participant_numbers.userid_to_number:
        return u""
    return """<li><a href="%s">%s</a></li>""" % ("%sclaim_participant_number" % api.meeting_url,
                                                 api.translate(_(u"Claim participant number")))

@view_action('user_info', 'participant_number', interface = IUser)
def participant_number_info(context, request, va, **kw):
    api = kw['api']
    if not api.meeting:
        return u""
    participant_numbers = request.registry.getAdapter(api.meeting, IParticipantNumbers)
    if context.userid not in participant_numbers.userid_to_number:
        return u""
    response = dict(
        api = api,
        number = participant_numbers.userid_to_number[context.userid],
        context = context)
    return render("templates/user_participant_number_info.pt", response, request = request)
