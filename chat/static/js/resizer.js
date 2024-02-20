var min = 300;
var max = 3600;
var mainmin = 300;

$('#split-bar').mousedown(function (e) {
    e.preventDefault();
    $(document).mousemove(function (e) {
        e.preventDefault();
        var x = e.pageX - $('#sidebar').offset().left;
        if (x > min && x < max && e.pageX < ($(window).width() - mainmin)) {
            $('#sidebar').css("width", x);
            $('#main').css("margin-left", x);
            document.querySelector(':root').style.setProperty("--sidebar-width", x);
        }
    })
});
$(document).mouseup(function (e) {
    $(document).unbind('mousemove');
});