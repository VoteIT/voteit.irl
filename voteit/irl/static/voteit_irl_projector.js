/* Projector prototype that handles projector view. */

function Projector() {
    this.tpl = $('#projector-pool .list-group-item').clone();
    this.filter_tpl = $('[data-filter-content] li').clone();
    this.tpl.removeClass('hidden');
    $('#projector-pool .list-group-item').remove();

    this.meetingUrl = $('#navbar-heading').attr('href');
    if (window.location.hash.length > 1) {
        var url = this.meetingUrl + window.location.hash + '/__ai_contents__.json';
        url = url.replace('#', '');
        this.load_context(url);
    }
    $('[data-toggle="tooltip"]').tooltip();

    $('body').on('click', '#projector-ai-menu a', this.handle_ai_menu_click.bind(this));
    $('body').on('click', '[data-nav-ai]', this.handle_ai_menu_click.bind(this));
    $('body').on('click', '[data-wf-state]', this.handle_wf_click.bind(this));
    $('body').on('click', '[data-quick-poll]', this.quick_poll.bind(this));
    $('body').on('click', '[data-tag-filter]', this.filter_tag.bind(this));
    $('body').on('click', '.move-left,.move-right', this.highlight_proposal_handler.bind(this));
    $('body').on('click', '.move-left,.move-right', this.highlight_proposal_handler.bind(this));
    $('body').on('click', '[data-filter-content]', function(e) { e.stopPropagation() });
    $('body').on('change', '[data-filter-content] input', this.filterChange.bind(this));
};

Projector.prototype = {

    load_context: function (url) {
        arche.do_request(url)
        .done(function(response) {
            this.handle_response(response);
            this.filterChange();
        }.bind(this));
    },

    handle_response: function (response) {
        this.reset();
        var filter_directive = {
            'li': {
                'obj<-workflow_states': {
                    'input@checked': 'obj.checked',
                    'input@name': 'obj.name',
                    'input@id': function(a) {
                        return 'filter-state-' + a.item.name;
                    },
                    'label': 'obj.title',
                    'label@for': function(a) {
                        return 'filter-state-' + a.item.name;
                    },
                    '.badge': 'obj.count',
                }
            }
        };
        var directive = {
            '.list-group-item': {
                'obj<-proposals': {
                    '.proposal-aid': function(a) {
                        return projector.linkify('#' + a.item['aid']);
                    },
                    '.proposal-text': function(a) {
                        return projector.linkify(a.item['text']);
                    },
                    '.proposal-author': 'obj.creator',
                    '[name="uid"]@value': 'obj.uid',
                    '.@data-uid': 'obj.uid',
                    '.@data-state': 'obj.wf_state',
                    '.@data-tags': 'obj.tags',
                    '[data-wf-state]@href': 'obj.prop_wf_url',
                    '[data-wf-state]@data-wf-state': function(a) {
                        return a.item['wf_state'];
                    },
                    '[data-state-indicator]@class+': function(a) {
                        return ' glyphicon-' + a.item['wf_state'] + ' text-' + a.item['wf_state'];
                    }
                },
                sort: function(a, b){
                    //Lazy version of ordering
                    var ordering = {'published': 1, 'approved': 2, 'denied': 3}
                    var cmp = function(x, y) {
                        return x > y? 1 : x < y ? -1 : 0;
                    }
                    return cmp(ordering[a.wf_state], ordering[b.wf_state]);
                }
            }
        };

        $('#projector-pool').render(response, directive);
        $('[data-filter-content]').render(response, filter_directive);
        $('#navbar-heading').attr('href', response['ai_regular_url']);

        $('[data-nav-ai="previous"]').attr('href', response['previous_url']);
        $('[data-nav-ai="previous"]').attr('title', response['previous_title']);
        if (response['previous_url']) {
            $('[data-nav-ai="previous"]').parent().removeClass('disabled');
        } else {
            $('[data-nav-ai="previous"]').parent().addClass('disabled');
        }
        $('[data-nav-ai="next"]').attr('href', response['next_url']);
        $('[data-nav-ai="next"]').attr('title', response['next_title']);
        if (response['next_url']) {
            $('[data-nav-ai="next"]').parent().removeClass('disabled');
        } else {
            $('[data-nav-ai="next"]').parent().addClass('disabled');
        }

        $('#navbar-heading').html(response['agenda_item']);
        try { window.history.pushState(null, response['agenda_item'], response['ai_url']); } catch(e) {}
    },

    handle_ai_menu_click: function (event) {
        event.preventDefault();
        var elem = $(event.currentTarget);
        if (!elem.parent().hasClass('disabled')) {
            this.load_context(elem.attr('href'));
        }
    },

    reset: function () {
        $('#projector-pool').html(this.tpl);
        $('#projector-main').empty();
        $('[data-filter-content]').html(this.filter_tpl);
    },

    handle_wf_click: function(event) {
        event.preventDefault();
        var elem = $(event.currentTarget);
        arche.do_request(elem.attr('href'), {method: 'POST', data: {state: elem.data('wf-state')}})
        .done(function(response) {
            this.handle_wf_response(event, response)
        }.bind(this));
    },

    handle_wf_response: function (event, response) {
        var elem = $(event.currentTarget);
        if (response['status'] == 'error') {
            arche.create_flash_message(response['msg'], {type: 'danger', 'auto_destruct': true})
        }
        if (response['status'] == 'success') {
            var controls = elem.parents('[data-wf-controls]');
            $(controls).children('[data-wf-state]').removeClass('active');
            $(controls).children('[data-wf-state="' + response['state'] + '"]').addClass('active')
        }
    },

    highlight_proposal_handler: function (event) {
        event.preventDefault();
        enable = $(event.currentTarget).hasClass('move-left');
        var elem = $(event.target).parents('.list-group-item');
        this.highlight_proposal(elem, enable);
    },

    highlight_proposal: function (elem, enable) {
        elem.remove()
        if (enable == true) {
            //Enable selection
            $('#projector-main').append(elem);
        } else {
            //Disable selection
            var last_pub = $('#projector-pool [data-state="published"]:last');
            if (elem.data('state') == 'published') {
                if (last_pub.length > 0) {
                    last_pub.after(elem);
                } else {
                    $('#projector-pool').prepend(elem);
                }
            } else {
                $('#projector-pool').append(elem);
            }
        }
    },

    /* Find all proposals currently placed in the highlighted section and post them */
    quick_poll: function (event) {
        event.preventDefault();
        $('[name="quick-poll-method"]').attr('value', $(event.currentTarget).data('quick-poll'));
        $('[name="reject-prop"]').attr('value', $(event.currentTarget).data('reject-prop'));
        var form = $('#quick-poll');
        arche.do_request(form.attr('action'), {'method': 'POST', 'data': form.serialize()})
        .done(function(response) {
            arche.load_flash_messages()
            arche.create_flash_message(response['msg'], {'type': 'success', 'auto_destruct': false})
            //FIXME: At least update ai item
        })
        .fail(function(jqXHR) {
            arche.flash_error(jqXHR);
        });
    },

    linkify: function(text) {
        var insert = '$1<a href="#" data-tag-filter="$2">$2</a>';
        return text.replace(/(^|\s)(#[a-z\d-_]+)/ig, insert);
    },

    filter_tag: function(event) {
        event.preventDefault();
        var elem = $(event.currentTarget);
        var select_tag = elem.data('tag-filter');
        if (select_tag[0] == '#') select_tag = select_tag.slice(1);
        //Unselect all
        $('#projector-main .list-group-item').each(function(i, v) {
            projector.highlight_proposal($(v), false);
        });
        //Select valid
        $('#projector-pool .list-group-item').each(function(i, v) {
        // note about lowercae: tags are always stored in lowercase!
            if ($.inArray( select_tag.toLowerCase() , $(v).data('tags').split(',') ) > -1) {
                projector.highlight_proposal($(v), true);
            }
        });
    },

    filterChange: function() {
        var workflow_states = [];
        $('[data-filter-content] input').each(function(i, e) {
            if (e.checked) { workflow_states.push(e.name); }
        });
        $('#projector-pool li').each(function(i, e) {
            $elem = $(e);
            if (workflow_states.indexOf($elem.data('state')) == -1) {
                $elem.addClass('hidden');
            } else {
                $elem.removeClass('hidden');
            }
        });
    }
}


$(function() {
    window.projector = new Projector();
});
