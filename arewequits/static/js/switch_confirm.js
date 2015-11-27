/*global $, jQuery*/
$('.switch-confirm').change(
    function () {
        'use strict';
        var del_in = $('#input_delete');
        if (del_in.prop('disabled')) {
            del_in.prop('disabled', false);
            del_in.removeClass('disabled');
            del_in.addClass('red');
        } else {
            del_in.prop('disabled', true);
            del_in.addClass('disabled');
            del_in.removeClass('red');
        }
    }
);
