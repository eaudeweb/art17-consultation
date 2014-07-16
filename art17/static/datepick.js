$(function() {
    var value_set = false;
    var start_date = $('#dp_start').datepicker().on('changeDate', function(evt) {
        if (!value_set || evt.date.valueOf() > end_date.date.valueOf()) {
            var newDate = new Date(evt.date)
            newDate.setDate(newDate.getDate() + 1);
            end_date.setValue(newDate);
        }
        start_date.hide();
        $('#dp_end')[0].focus();
    }).data('datepicker');
    var end_date = $('#dp_end').datepicker({
        onRender: function(date) {
            return date.valueOf() <= start_date.date.valueOf() ? 'disabled' : '';
        }
    }).on('changeDate', function(evt) {
        end_date.hide();
        value_set = true;
    }).data('datepicker');
});
