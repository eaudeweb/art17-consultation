$(function() {
    $('select.semaphore').on('change', function() {
        $(this).attr('data-color', $(this).val());
    }).change();
});
