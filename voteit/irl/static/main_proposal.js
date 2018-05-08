
var main_proposal = {
    clickHandler: function(e) {
        e.preventDefault();
        $button = $(e.currentTarget);
        do_request($button.attr('href'), {
            'method': 'POST',
            'data': {'state': !$button.hasClass('active')},
        })
        .done(function(data) {
            if (data.new_state) {
                $button.addClass('active');
            } else {
                $button.removeClass('active');
            }
            $button.parents('[data-uid]').find('[data-collapsible-text] > span').html(data.new_text);
        });
    }
};

$(function() {
    $('body').on('click', '[data-main-proposal]', main_proposal.clickHandler)
});
