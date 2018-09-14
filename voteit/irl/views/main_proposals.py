# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from pyramid.view import view_config

from voteit.core import security
from voteit.core.models.interfaces import IProposal
from voteit.core.views.control_panel import control_panel_link
from voteit.irl import _


def _check_tag_in_text(tag_name, text):
    # type: (unicode, unicode) -> bool
    return bool(re.search(r'(\A|\s)#{}\s'.format(tag_name), text, re.UNICODE | re.IGNORECASE))


@view_action('metadata_listing', 'main_proposal',
             permission=security.VIEW,
             interface=IProposal,
             priority=50)
def main_property_action(context, request, va, **kw):
    hashtag_name = request.meeting.main_proposal_hashtag_name
    if hashtag_name:
        response = {'context': context,
                    # 'main_proposal': main_proposal,
                    'active': hashtag_name.lower() in context.tags}
        return render('voteit.irl:templates/main_proposal_btn.pt', response, request=request)


@view_config(name="main_proposals_settings",
             permission=security.MODERATE_MEETING,
             renderer="arche:templates/form.pt")
class MainProposalsSettingsForm(DefaultEditForm):
    schema_name = 'main_proposals_settings'
    title = _('Main proposals')


@view_config(
    context=IProposal,
    name='__set_main_proposal__',
    permission=security.MODERATE_MEETING,
    renderer='json',
)
def MainProposalSetView(context, request):
    tag_name = request.meeting.main_proposal_hashtag_name
    state = request.POST.get('state') == 'true'
    if tag_name:
        tag_exists = _check_tag_in_text(tag_name, context.text)
        if state and not tag_exists:
            context.update(text='#{} {}'.format(tag_name, context.text))
        elif tag_exists:
            context.update(text=context.text.replace('#' + tag_name, '').strip())
    return {
        'new_state': state,
        'new_text': request.render_proposal_text(context),
    }


def includeme(config):
    # Set property on meeting
    from voteit.core.models.meeting import Meeting
    def get_main_proposal_hashtag_name(self):
        return self.get_field_value('main_proposal_hashtag_name')
    def set_main_proposal_hashtag_name(self, value):
        return self.set_field_value('main_proposal_hashtag_name', value)
    Meeting.main_proposal_hashtag_name = property(get_main_proposal_hashtag_name, set_main_proposal_hashtag_name)

    config.scan(__name__)
    config.add_view_action(
        control_panel_link,
        'control_panel_proposal', 'main_proposals',
        title=_("Main proposals"),
        view_name='main_proposals_settings',
    )
