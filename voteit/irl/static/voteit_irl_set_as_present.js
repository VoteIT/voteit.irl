
$('#register_set_attending').live('click', function(event) {
    /* stop form from submitting normally 
    IE might throw an error calling preventDefault(), so use a try/catch block. */
    try { event.preventDefault(); } catch(e) {}
    var status_area = $('#register_current_status');
    spinner().appendTo(status_area);
    var url = $(this).attr('href');
    //var url = 'ksdnfjs'; ////
    status_area.load(url, function(response, status, xhr) {
        if (status == "error") {
            //There's currently no JS function for adding flash messages. We should have one!
            _mk_flash_message(voteit.translation['register_meeting_presence_error_notice'], 'error');
        }
        else {
            _mk_flash_message(voteit.translation['presence_success_notice'], 'info');
        }
    });
    status_area.find('img.spinner').remove();
});


function _mk_flash_message(msg, status) {
    // Should be a function within voteit common :)
    if ((status == 'error') && ($('#flash_messages .error').length != 0))
        return;
    var output = '<div class="' + status + ' message"><span>';
    output += msg
    output += '</span><a href="" class="close_message">X</a></div>';
    $('#flash_messages .clear').before(output);
}
