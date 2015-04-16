
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
});
