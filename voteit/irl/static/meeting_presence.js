
$(document).ready(function() {
  if (typeof voteit.watcher === 'undefined') {
    voteit.watcher = new Watcher();
  }
  function presence_callback(response) {
    if (typeof response['meeting_presence'] !== 'undefined') {
      if (response['meeting_presence']['status'] == 'open' && $('#meeting-presence-notification').length == 0) {
        arche.create_flash_message(response['meeting_presence']['msg'], {id: 'meeting-presence-notification', slot: 'fixed-msg-bar', auto_destruct: false, type: 'success'});
      } 
      if (response['meeting_presence']['status'] == 'closed' && $('#meeting-presence-notification').length != 0) {
        $('#meeting-presence-notification').remove();
      }
    }
  };
  //The watcher itself will be started from VoteIT core if it's needed
  voteit.watcher.add_response_callback(presence_callback);
});
