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


    $('select[name="population.size.population.unit"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="populationlink.size.population.unit"]').val(text);
    }).change();
    $('input[name="population.size.population.min"]').on('change', function() {
        var value = $(this).val();
        $('input[name="populationlink.size.population.min"]').val(value);
    }).change();
    $('input[name="population.size.population.max"]').on('change', function() {
        var value = $(this).val();
        $('input[name="populationlink.size.population.max"]').val(value);
    }).change();


    $('select[name="population.size.population_alt.unit"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="populationlink.size.population_alt.unit"]').val(text);
    }).change();
    $('input[name="population.size.population_alt.min"]').on('change', function() {
        var value = $(this).val();
        $('input[name="populationlink.size.population_alt.min"]').val(value);
    }).change();
    $('input[name="population.size.population_alt.max"]').on('change', function() {
        var value = $(this).val();
        $('input[name="populationlink.size.population_alt.max"]').val(value);
    }).change();

    // habitats

    $('select[name="coverage.conclusion.value"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="coveragelink.conclusion.value"]').val(text);
    }).change();
    $('select[name="coverage.conclusion.trend"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="coveragelink.conclusion.trend"]').val(text);
    }).change();

    $('select[data-speciallink="habitatrange.conclusion.value"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="habitatrangelink.conclusion.value"]').val(text);
    }).change();
    $('select[data-speciallink="habitatrange.conclusion.trend"]').on('change', function() {
        var text = $(this).find('option:selected').text();
        $('input[name="habitatrangelink.conclusion.trend"]').val(text);
    }).change();
});
