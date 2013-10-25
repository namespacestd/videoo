/** main.js
 * Javascript functions for Videe-o web application.
 * Functions based on JQuery are initialized upon form load.  Most functions
 * check to make sure certain controls exist on the page before they execute. */

/* Use strict mode: this makes it so the javascript is validated by the browser
 * according to ECMAScript 5 standards. This must be the first statement in the javascript
 * file to work. */
'use strict';

/* This first function initializes all javascript functions as soon as JQuery is initialized
 * in the page. */
$(document).ready(function () {
    _initializeSearchBox();
});

/* Initialize search form that appears at the top of each page */
function _initializeSearchBox() {

    // Each time the search term is changed, check to see if the search term is 2 characters or longer. If so,
    // enable the submit button.
    $('#search input[name=q]').keyup(function() {
        if ($('#search input[name=q]').val().length < 2) {
            $('#search button').attr('disabled', 'disabled');
        }
        else {
            $('#search button').removeAttr('disabled');
        }
    });
    $('#search button').attr('disabled', 'disabled'); // It should start out disabled, since it starts empty

    // If the current search term is less than 2 characters, prevent the form from submitting
    $('#search').submit(function (e) {
        if (len($('#search input[name=q]')) < 2) {
            e.preventDefault();
        }
    });
}