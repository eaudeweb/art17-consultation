jQuery.fn.DataTable.ext.type.search.string = function ( data ) {
    return ! data ?
        '' :
        typeof data === 'string' ?
            data
                .replace( /έ/g, 'ε')
                .replace( /ύ/g, 'υ')
                .replace( /ό/g, 'ο')
                .replace( /ώ/g, 'ω')
                .replace( /ά/g, 'α')
                .replace( /ί/g, 'ι')
                .replace( /ή/g, 'η')
                .replace( /\n/g, ' ' )
                .replace( /á/g, 'a' )
                .replace( /é/g, 'e' )
                .replace( /í/g, 'i' )
                .replace( /ó/g, 'o' )
                .replace( /ú/g, 'u' )
                .replace( /ê/g, 'e' )
                .replace( /î/g, 'i' )
                .replace( /ô/g, 'o' )
                .replace( /è/g, 'e' )
                .replace( /ï/g, 'i' )
                .replace( /ü/g, 'u' )
                .replace( /ç/g, 'c' )
                .replace( /ă/g, 'a' )
                .replace( /â/g, 'a' )
                .replace( /ș/g, 's' )
                .replace( /t/g, 't' )
                .replace( /ì/g, 'i' ) :
            data;
};
