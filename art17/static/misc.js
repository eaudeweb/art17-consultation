$(function() {
    $('select.semaphore').on('change', function() {
        $(this).attr('data-color', $(this).val());
    }).change();

    $('select[name="range.conclusion.value"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="rangelink.conclusion.value"]').val(text);
    }).change();

    $('select[name="range.conclusion.trend"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="rangelink.conclusion.trend"]').val(text);
    }).change();


    $('select[name="population.conclusion.value"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="populationlink.conclusion.value"]').val(text);
    }).change();

    $('select[name="population.conclusion.trend"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="populationlink.conclusion.trend"]').val(text);
    }).change();


    $('select[name="habitat.conclusion.value"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="habitatlink.conclusion.value"]').val(text);
    }).change();

    $('select[name="habitat.conclusion.trend"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="habitatlink.conclusion.trend"]').val(text);
    }).change();
});
