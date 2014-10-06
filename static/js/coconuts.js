/**
 * Created with PyCharm.
 * User: marc
 * Date: 10/5/14
 * Time: 9:44 PM
 * To change this template use File | Settings | File Templates.
 */

// wait for the DOM to be loaded
$(document).ready(function() {
    // bind 'find-paths' and provide a simple callback function
    $('#find-paths').submit(function(e) {
        $.get( "?dist="+$('#dist').val(), function( data ) {
          $( "#results" ).html( data );
        });
        e.preventDefault();
    });
});