$(document).ready(function () {
    // Support
    $("#support").on("input",function(){
        $("#span_support").text($('#support')[0].value);
    });
    // Confidence
    $("#confidence").on("input",function(){
        $("#span_confidence").text($('#confidence')[0].value);
    });
    // Lift
    $("#lift").on("input",function(){
        $("#span_lift").text($('#lift')[0].value);
    });
});