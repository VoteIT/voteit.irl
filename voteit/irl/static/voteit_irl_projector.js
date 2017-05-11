/* Projector prototype that handles projector view. */

var Projector = function() {
  this.tpl = $('#projector-pool .list-group-item').clone();
  this.tpl.removeClass('hidden');
  $('#projector-pool .list-group-item').remove();
};

Projector.prototype.load_context = function (url) {
  var request = arche.do_request(url);
  var that = this;
  request.done(function(response) {
    that.handle_response(response);
  });
}

Projector.prototype.handle_response = function (response) {
  this.reset();
  var directive = {'.list-group-item':
    {'obj<-proposals':
      {'.proposal-aid': 'obj.aid',
       '.proposal-text': 'obj.text',
       '.proposal-author': 'obj.creator',
       '[name="uid"]@value': 'obj.uid',
       '.@data-uid': 'obj.uid',
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
      }
    }
  };
  $('#projector-pool').render(response, directive);

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

Projector.prototype.handle_ai_menu_click = function (event) {
  event.preventDefault();
  var elem = $(event.currentTarget);
  if (!elem.parent().hasClass('disabled')) {
    this.load_context(elem.attr('href'));
  }
}

Projector.prototype.reset = function () {
  $('#projector-pool').html(this.tpl);
  $('#projector-main').empty();
}

Projector.prototype.handle_wf_click = function(event) {
  event.preventDefault();
  var elem = $(event.currentTarget);
  var request = arche.do_request(elem.attr('href'), {method: 'POST', data: {state: elem.data('wf-state')}});
  var that = this;
  request.done(function(response) {
    that.handle_wf_response(event, response)
  });
}

Projector.prototype.handle_wf_response = function (event, response) {
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

Projector.prototype.highlight_proposal = function (event, enable) {
  event.preventDefault();
  var elem = $(event.target).parents('.list-group-item');
  elem.remove()
  if (enable == true) {
    //Enable selection
    $('#projector-main').append(elem);
  } else {
    //Disable selection
    $('#projector-pool').append(elem);
  }
}

/* Find all proposals currently placed in the highlighted section and post them */
Projector.prototype.quick_poll = function (event) {
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
