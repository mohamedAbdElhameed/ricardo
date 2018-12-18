/*global $, jQuery, alert*/
$(document).ready(function () {
    
    "use strict";
    
    ///////////.header//////////////
    $('.header').height($(window).height());
    
    /////#search_show///////
    $('#search_show').click(function () {
        
        $('i#search_show').toggleClass('fa-close');
        $('.search-form-box').toggle();
        
    });
    
    /////.login-wrap///////
    $('#login_show').click(function () {
        
        $('i#login_show').toggleClass('fa-close');
        $('.login-wrap').toggle();
        
    });
    
    // Hide Placeholder On Form Focus

	$('[placeholder]').focus(function () {

		$(this).attr('data-text', $(this).attr('placeholder'));

		$(this).attr('placeholder', '');

	}).blur(function () {

		$(this).attr('placeholder', $(this).attr('data-text'));

	});
    
    /////.skitter///////
    $('.skitter-large').skitter({
        thumbs: true,
        dots: false
    });
    
    
});

// ////File Navbar Responsive//////
function openNav() {
    "use strict";
    document.getElementById("mySidenav").style.width = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
}

function closeNav() {
    "use strict";
    document.getElementById("mySidenav").style.width = "0";
    document.body.style.backgroundColor = "white";
}



