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
    var html = $('<div>').attr('class', 'row');
    var pressure = $('select[name="pressures.add_pressure"]').val();
    var ranking = $('select[name="pressures.add_ranking"]').val();
    var pollution = $('select[name="pressures.add_pollution"]').val();
    var data = {pressure: pressure, ranking: ranking, pollution: pollution};

    $('<input>').attr({
        type: "hidden",
        name: "pressures.add_data",
        value: JSON.stringify(data)
    }).appendTo('form');

    $('<div>').attr("class", "col-sm-2").html(pressure).appendTo(html);
    $('<div>').attr("class", "col-sm-2").html(ranking).appendTo(html);
    $('<div>').attr("class", "col-sm-2").html(pollution).appendTo(html);

    var actions = $('<div>').attr("class", "col-sm-2");
    $('<button>').attr({
        class: "close hidepressure",
        type: "button"
    }).html('&times;').appendTo(actions);
    actions.appendTo(html);

    html.appendTo('#pressures_container');
});

$('body').on('click', '.hidepressure', function(evt) {
  evt.preventDefault();
  $(this).parent().parent().remove();
});

})();
