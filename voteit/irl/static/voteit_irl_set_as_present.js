
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
            $('#meeting_presence_msg').text(voteit.translation['register_meeting_presence_error_notice']).addClass('error');
        }
    });
    status_area.find('img.spinner').remove();
});
