(function() {

"use strict";

var recorddetail = $('#recorddetail-modal');

$('.records-detailbtn').click(function(evt) {
  evt.preventDefault();
  var url = $(this).data('url');

  recorddetail.modal('hide');
  set_html("<h1>Se încarcă...</h1>");
  $.get(url).done(set_html);
  recorddetail.modal();
});

function set_html(html) {
  var title = recorddetail.find('.modal-title');
  var body = recorddetail.find('.modal-body');
  body.html(html);
  var h1 = body.find('h1').remove();
  title.empty().append(h1.html());
}

$('body').on('click', '.showmap', function(evt) {
  evt.preventDefault();
  var link = $(this);
  var url = link.attr('href');
  var title = "Hartă";
  var params = 'height=650,width=850,screenX=100,screenY=100';
  var popup = window.open(url, title, params);
  popup.focus();
});

$('.add-pressuresbtn').click(function(evt) {
    evt.preventDefault();
    var container = $(this).parent().parent();
    var html_container = $(this).data('container');
    var html = $('<tr>');
    var pressure = container.find('select[name="addform_pressure.pressure"]').val();
    var pressure_text = container.find('select[name="addform_pressure.pressure"] option:selected').text();
    var ranking = container.find('select[name="addform_pressure.ranking"]').val();
    var ranking_text = container.find('select[name="addform_pressure.ranking"] option:selected').text();
    var pollutions = container.find('select[name="addform_pressure.pollutions"]').val();
    var pressure_pollutions = []
    container.find('select[name="addform_pressure.pollutions"] option:selected').each(function(i, selected){
      pressure_pollutions[i] = $(selected).text();
    });

    var pollutions_text = pressure_pollutions.join();
    var data;

    if (!pressure) {
        return alert('Nu ați selectat presiunea');
    }
    if (!ranking) {
        return alert('Nu ați selectat clasificarea');
    }
    if (!pollutions) {
        data = {pressure: pressure, ranking: ranking, pollutions: ''};
    } else {
        data = {pressure: pressure, ranking: ranking, pollutions: pollutions};
    }

    $('<input>').attr({
        type: "hidden",
        name: $(this).data('inputname'),
        value: JSON.stringify(data)
    }).appendTo('form');

    $('<td>').html(pressure_text).appendTo(html);
    $('<td>').html(ranking_text).appendTo(html);
    $('<td>').html(pollutions_text).appendTo(html);

    var actions = $('<td>');
    $('<button>').attr({
        class: "btn btn-danger btn-sm hidepressure",
        type: "button"
    }).html('șterge').appendTo(actions);
    actions.appendTo(html);

    $(html_container + ' tr:last').before(html);

    // reset form
    $('select[name="addform_pressure.pressure"]').val('');
    $('select[name="addform_pressure.ranking"]').val('');
    $('select[name="addform_pressure.pollutions"] option:selected').removeAttr('selected');
});

$('body').on('click', '.hidepressure', function(evt) {
  evt.preventDefault();
  if (confirm('Sunteți sigur că vreți să ștergeți această înregistrare?')) {
      $(this).parent().parent().remove();
  }
});

$('.add-measurebtn').click(function(evt) {
    evt.preventDefault();

    var html = $('<tr>');
    var data = {};
    var valid = true;

    $('#measuresform').find('select.form-control').each(function () {
        var name = $(this).attr('name');
        name = name.substr(name.indexOf('.') + 1);

        if (valid && !$(this).val()) {
          if (name == 'measurecode') {
            alert('Vǎ rugǎm selectați o valoare pentru mǎsurǎ');
          }
          else if (name == 'rankingcode') {
            alert('Vǎ rugǎm selectați o valoare pentru importanțǎ');
          }
          valid = false;
        }
    });
    if (!valid)
        return;

    $('#measuresform').find('.form-control').each(function () {
        var name = $(this).attr('name');
        var html_data = '';
        name = name.substr(name.indexOf('.') + 1);

        if ($(this).is('input')) {
            data[name] = $(this).is(':checked')?'1':'0';
            html_data = $('<input>').attr({
                disabled: "disabled",
                type: "checkbox",
                checked: $(this).is(':checked')
            });
            $(this).attr('checked', false);
        } else {
            data[name] = $(this).val();
            html_data = $(this).find('option:selected').text();
            $(this).val('');
        }
        $('<td>').html(html_data).appendTo(html);
    });
    var actions = $('<td>');
    $('<button>').attr({
        class: "btn btn-danger btn-sm hidepressure",
        type: "button"
    }).html('șterge').appendTo(actions);

    actions.appendTo(html);
    $('#measures_container tr:last').before(html);
    $('<input>').attr({
        type: "hidden",
        name: "measures.measures",
        value: JSON.stringify(data)
    }).appendTo('form');
});

})();
