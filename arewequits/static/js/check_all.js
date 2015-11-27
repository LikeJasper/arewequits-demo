/*global $, jQuery*/
$('#id_check_all_who_for_button').click(
    function () {
        'use strict';
        if ($(this).text() === "Uncheck all") {
            $('input:checkbox[name=who_for]').prop('checked', false);
            $(this).text("Check all");
        } else if ($(this).text() === "Check all") {
            $('input:checkbox[name=who_for]').prop('checked', true);
            $(this).text("Uncheck all");
        }
    }
);
$('input:checkbox').change(
    function () {
        'use strict';
        var boxes = $(':checkbox[name=who_for]').length,
            checked = $(':checkbox[name=who_for]:checked').length;
        if (checked === boxes) {
            $('#id_check_all_who_for_button').text("Uncheck all");
        } else {
            $('#id_check_all_who_for_button').text("Check all");
        }
    }
);