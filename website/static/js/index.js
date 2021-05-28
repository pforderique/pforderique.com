// will this dynamically change active link for navbar?
$(document).ready(function () {
    var url = window.location;
    // $('nav.navbar a[href="'+ url +'"]').addClass('active');
    $('nav.navbar a').filter(function() {
         return this.href == url;
    }).addClass('active');
}); 