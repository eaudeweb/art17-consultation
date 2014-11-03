$( function () {
  $('tfoot').hide();

  $('#dt-filter').click(function() {
    $('tfoot').toggle();
  });
});

function enable_filtering(table_id) {
  $(table_id + ' tfoot th.searchable').each( function () {
    var title = $(table_id + ' thead th').eq( $(this).index() ).text();
    $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
  });

  // DataTable
  var table = $(table_id).DataTable({
    paging: false,
  });

  $('.dataTables_filter').hide();

  // Apply the search
  table.columns().eq( 0 ).each( function ( colIdx ) {
    $( 'input', table.column( colIdx ).footer() ).on( 'keyup change', function () {
      table
        .column( colIdx )
        .search( this.value )
        .draw();
      });
  });
}
