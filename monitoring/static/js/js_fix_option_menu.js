$(function () {
    $('body')
        .on('click', '#participant,#duples,#reports,#configuration,#organization,#catalogs,#security', function () {
            let parent = $(this).parent();
            if (parent.hasClass('menu-open')) {
                parent.removeClass('menu-open');
                parent.children('ul').fadeOut('slow');
            } else {
                parent.addClass('menu-open');
                parent.children('ul').fadeIn('slow');
            }
        })
        .on('click', '#icon_menu', function () {
            let body = $('body');
            if (body.hasClass('sidebar-collapse')) {
                body.removeClass('sidebar-collapse');
            } else {
                body.addClass('sidebar-collapse');
            }
        })
        .on('click', '#exitOption', function () {
            let parent = $(this).parent();
            if (parent.hasClass('menu-open')) {
                parent.removeClass('menu-open');
                parent.children('ul').removeClass('show');
            } else {
                parent.addClass('menu-open');
                parent.children('ul').addClass('show');
            }
        })
});