/*global $, document, jQuery*/
$(document).ready(function () {
    'use strict';
    $('#id_help_button_payments').tooltipster({
        position: 'top-left',
        trigger: 'custom',
        content: $('<h3 class="payment-help">How to add a payment</h3>' +
            '<p class="payment-help"><em>Step 1:</em> Select the date and enter the amount.</p>' +
            '<p class="payment-help"><em>Step 2:</em> Pick an icon to identify what kind of payment it is.</p>' +
            '<p class="payment-help"><em>Step 3:</em> Add a short description so people know what it is.</p>' +
            '<p class="payment-help"><em>Step 4:</em> Select who paid.  This doesn\'t have to be you - ' +
            'you can always record payments that your friends made.</p>' +
            '<p class="payment-help"><em>Step 5:</em> Select everyone who benefited from the payment. ' +
            'Don\'t forget to select yourself if you also benefited!</p>')
    });
    $('.tooltip-bottom').tooltipster({
        position: 'bottom',
        trigger: 'custom'
    });
    $('.tooltip-left').tooltipster({
        position: 'left',
        trigger: 'custom'
    });
    $('.tooltip-right').tooltipster({
        position: 'right',
        trigger: 'custom'
    });
    $('.tooltip-top-left').tooltipster({
        position: 'top-left',
        trigger: 'custom'
    });
    $('.tooltip').tooltipster({
        trigger: 'custom'
    });
});
$('.help-button').hover(
    function () {
        'use strict';
        $('.tooltip').tooltipster('show');
    },
    function () {
        'use strict';
        $('.tooltip').tooltipster('hide');
    }
);
$('.help-button').click(
    function () {
        'use strict';
        if ($('.tooltipster-base').length) {
            $('.tooltip').tooltipster('hide');
        } else {
            $('.tooltip').tooltipster('show');
        }
    }
);
