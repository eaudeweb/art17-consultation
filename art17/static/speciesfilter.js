(function() {

"use strict";

var speciesfilter = $('.speciesfilter');

var group_select = speciesfilter.find('[name=group]').select2({
  data: App.species_groups,
  minimumResultsForSearch: -1,  // disable search field
  width: '10em'
});


var species_select = speciesfilter.find('[name=species]');

function update_species_select(group_id) {
  var group_id = group_select.select2('val');
  var species_in_group = _(App.species_list).filter(
      function(sp){return sp.group_id == group_id});

  species_select.select2('destroy').select2({
    data: species_in_group,
    multiple: false,
    width: '25em'
  });
}

update_species_select();

speciesfilter.change(function() {
  update_species_select();
});

})();
