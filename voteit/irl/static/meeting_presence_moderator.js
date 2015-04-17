
function handle_add_as_present_form(event) {
  event.preventDefault();
  var form = $(event.target);
  if ($('[name="userid_or_pn"]').val() == '') return false;
  var request = arche.do_request(form.attr('action'), {data: form.serialize(), method: 'POST'});
  request.done(handle_add_as_present_response);
  request.fail(arche.flash_error);
}

function handle_add_as_present_response(response) {
  if (response['status'] == 'error') {
    arche.create_flash_message(response['msg'], {type: 'danger', auto_destruct: true});
  } else {
    arche.create_flash_message(response['msg'], {type: response['status'], auto_destruct: true});
    $('[name="userid_or_pn"]').val('').focus();
    if (typeof response['count'] !== 'undefined') {
      $('[data-meeting-presence-count]').html(response['count']);
    }
  }
}

$(document).ready(function() {
  if (typeof voteit.watcher === 'undefined') {
    voteit.watcher = new Watcher();
  }
  function presence_moderator_callback(response) {
    if (typeof response['meeting_presence_count'] !== 'undefined') {
      $('[data-meeting-presence-count]').html(response['meeting_presence_count']);
    }
  };
  //The watcher itself will be started from VoteIT core if it's needed
  voteit.watcher.add_response_callback(presence_moderator_callback);
  
  $('#add_as_present').on('submit', handle_add_as_present_form);
});
