$( function () {
  $('thead.thead').hide();

  $('#dt-filter').click(function() {
    $('thead.thead').toggle();
  });
});

function enable_filtering(table_id) {
  $(table_id + ' thead th.searchable').each( function () {
    var title = $(table_id + ' thead th').eq( $(this).index() ).text();
    $(this).html( '<input type="text" placeholder="Filtreaza '+title+'" />' );
  });

  // DataTable
  var table = $(table_id).DataTable({
    paging: false
  });

  $('.dataTables_filter').hide();
  $('.dataTables_info').hide();
  $('.dataTables_empty').parent().parent().hide();

  // Apply the search
  table.columns().eq( 0 ).each( function ( colIdx ) {
    $(table_id + ' thead.thead input').eq( colIdx ).on( 'keyup change', function () {
      table
        .column( colIdx )
        .search(
            jQuery.fn.DataTable.ext.type.search.string( this.value )
        )
        .draw();
      });
  });
}
