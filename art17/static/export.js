$(function () {
    $('.download-button').click(function (evt) {
        evt.preventDefault();
        export_current();
    });
});

function export_current() {
    var html = $('body').html();
    var url = '/export_excel/';
    var form = $('<form>', {
        'action': url,
        'method': 'POST'
    });
    var html_input = $('<input>', {
        'type': 'hidden',
        'name': 'html'
    });
    html_input.val(html);
    html_input.appendTo(form);
    form.appendTo('body');
    form.submit();
}
