/* Projector prototype that handles projector view. */

var Projector = function() {
  this.tpl = "";
  this.init = function() {
      this.tpl = $('#projector-pool .list-group-item').clone();
      this.tpl.removeClass('hidden');
      $('#projector-pool .list-group-item').remove();
  }

  this.load_context = function (url) {
    var request = arche.do_request(url);
    var that = this;
    request.done(function(response) {
        that.handle_response(response);
    });
  }

  this.linkify = function(text) {
    var insert = '$1<a href="#" data-tag-filter="$2">$2</a>';
    return text.replace(/(^|\s)(#[a-z\d-_]+)/ig, insert);
  }

  this.filter_tag = function(event) {
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
  }

  this.handle_response = function (response) {
      this.reset();
      var directive = {'.list-group-item':
        {'obj<-proposals':
          {'.proposal-aid': function(a) {
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
           '[data-wf-state="published"]@class+': function(a) {
             if (a.item['wf_state'] == "published") {
               return ' active';
             }
           },
           '[data-wf-state="approved"]@class+': function(a) {
             if (a.item['wf_state'] == "approved") {
               return ' active';
             }
           },
           '[data-wf-state="denied"]@class+': function(a) {
             if (a.item['wf_state'] == "denied") {
               return ' active';
             }
           },
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
    }

    this.handle_ai_menu_click = function (event) {
      event.preventDefault();
      var elem = $(event.currentTarget);
      if (!elem.parent().hasClass('disabled')) {
        this.load_context(elem.attr('href'));
      }
    }

    this.reset = function () {
      $('#projector-pool').html(this.tpl);
      $('#projector-main').empty();
    }

    this.handle_wf_click = function(event) {
      event.preventDefault();
      var elem = $(event.currentTarget);
      var request = arche.do_request(elem.attr('href'), {method: 'POST', data: {state: elem.data('wf-state')}});
      var that = this;
      request.done(function(response) {
        that.handle_wf_response(event, response)
      });
    }

    this.handle_wf_response = function (event, response) {
      var elem = $(event.currentTarget);
      if (response['status'] == 'error') {
        arche.create_flash_message(response['msg'], {type: 'danger', 'auto_destruct': true})
      }
      if (response['status'] == 'success') {
        var controls = elem.parents('[data-wf-controls]');
        $(controls).children('[data-wf-state]').removeClass('active');
        $(controls).children('[data-wf-state="' + response['state'] + '"]').addClass('active')
      }
    }

    this.highlight_proposal_handler = function (event, enable) {
        event.preventDefault();
        var elem = $(event.target).parents('.list-group-item');
        this.highlight_proposal(elem, enable);
    }

    this.highlight_proposal = function (elem, enable) {
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
    }

    /* Find all proposals currently placed in the highlighted section and post them */
    this.quick_poll = function (event) {
        event.preventDefault();
        $('[name="quick-poll-method"]').attr('value', $(event.currentTarget).data('quick-poll'));
        $('[name="reject-prop"]').attr('value', $(event.currentTarget).data('reject-prop'));
        var form = $('#quick-poll');
        var request = arche.do_request(form.attr('action'), {'method': 'POST', 'data': form.serialize()});
        request.done(function(response) {
            arche.load_flash_messages()
            arche.create_flash_message(response['msg'], {'type': 'success', 'auto_destruct': false})
            //FIXME: At least update ai item
        });
        request.fail(function(jqXHR) {
            arche.flash_error(jqXHR);
        });
    }

};


var projector = new Projector();


$(document).ready(function() {
    projector.init();
    $('body').on('click', '#projector-ai-menu a', function(event) {
        projector.handle_ai_menu_click(event);
    });
    $('body').on('click', '[data-nav-ai]', function(event) {
        projector.handle_ai_menu_click(event);
    });
    $('body').on('click', '.move-left', function(event) {
      projector.highlight_proposal_handler(event, true);
    });
    $('body').on('click', '.move-right', function(event) {
      projector.highlight_proposal_handler(event, false);
    });
    $('body').on('click', '[data-wf-state]', function(event) {
        projector.handle_wf_click(event);
    });
    $('body').on('click', '[data-quick-poll]', projector.quick_poll);

    $('body').on('click', '[data-tag-filter]', function(event) {
        projector.filter_tag(event);
    });
});
