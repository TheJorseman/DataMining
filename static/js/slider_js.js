$(document).ready(function () {
    // Support
    $("#support").on("input",function(){
        $("#support_input").val($('#support')[0].value);
    });
    $("#support_input").on("input",function(){
        $("#support").val($('#support_input')[0].value);
    });

    $("#support_input").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsgs").html("Solo se admiten digitos").show().fadeOut("slow");
                  return false;
       }
    });
    // Confidence
    $("#confidence").on("input",function(){
        $("#confidence_input").val($('#confidence')[0].value);
    });
    $("#confidence_input").on("input",function(){
        $("#confidence").val($('#confidence_input')[0].value);
    });
    $("#confidence_input").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsgc").html("Solo se admiten digitos").show().fadeOut("slow");
                  return false;
       }
    });
    // Lift
    $("#lift").on("input",function(){
        $("#lift_input").val($('#lift')[0].value);
    });
    $("#lift_input").on("input",function(){
        $("#lift").val($('#lift_input')[0].value);
    });
    $("#lift_input").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsgl").html("Solo se admiten digitos").show().fadeOut("slow");
                  return false;
       }
    });
});