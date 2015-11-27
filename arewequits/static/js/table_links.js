/*global $, window, jQuery*/
$('.clickable-row').click(function () {
    'use strict';
    window.document.location = $(this).data('url');
});