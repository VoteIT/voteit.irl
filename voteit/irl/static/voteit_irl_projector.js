// Bind to menu function
$('.dropdown_menu .menu_header').live('hover', function(event) { dropdown_menus(event, this, '') });

$('a.activate').live('click', function(event) {
    try { event.preventDefault(); } catch(e) {}
    $(this).parents('li').appendTo($('#active > ul'));
});
$('a.inactivate').live('click', function(event) {
    try { event.preventDefault(); } catch(e) {}
    $(this).parents('li').appendTo($('#inactive > ul'));
});
$('.states a').live('click', function(event) {
    try { event.preventDefault(); } catch(e) {}
    var url = $(this).attr("href");
    var li = $(this).parents('li');
    $.get(url, function(data) {
        li.replaceWith(data)
    });
});
