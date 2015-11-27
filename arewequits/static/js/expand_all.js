/*global $, jQuery*/
$('#id_expand_all_payments_button').click(
    function () {
        'use strict';
        if ($(this).text() === "Expand all") {
            $('.collapsible li').addClass('active');
            $('.collapsible-header').addClass('active');
            $('.collapsible-body').show();
            $(this).text("Collapse all");
        } else if ($(this).text() === "Collapse all") {
            $('.collapsible li').removeClass('active');
            $('.collapsible-header').removeClass('active');
            $('.collapsible-body').hide();
            $(this).text("Expand all");
        }
    }
);
$('.collapsible li').click(
    function () {
        'use strict';
        var headers = $('.collapsible-header').length,
            active = $('.collapsible-header.active').length;
        if (active === headers) {
            $('#id_expand_all_payments_button').text("Collapse all");
        } else {
            $('#id_expand_all_payments_button').text("Expand all");
        }
    }
);