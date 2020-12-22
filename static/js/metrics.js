$(document).ready(function () {

    $("#show_distance_matrix").click(function(){
        var form = new FormData();
        form.append("metric",$("#metric").val());
        form.append("minkowski_coef",$('#minkowski_coef')[0].value);
        console.log("distance");
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/calc_distance',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#distance_table_container").html(response["distance_table"]);
            },
            error: function(error){
                console.log(error);
            }
        });  
        $("#js-loader").css("display","none");
        $("#export").css("display","block");
    });


    $('#metric').on('change', function() {
        if (this.value == "minkowski"){
            $("#minkowski_value").css("display","block");
        }else{
            $("#minkowski_value").css("display","none");
        }
    });

    $("#minkowski_coef").keypress(function (eve) {

        if ((eve.which != 46 || $(this).val().indexOf('.') != -1) && (eve.which < 48 || eve.which > 57) || (eve.which == 46 && $(this).caret.start == 0)) {
            eve.preventDefault();
            $("#span_minkowski_coef").html("Solo se admiten digitos").show().fadeOut("slow");
            return false;
        }
        // this part is when left part of number is deleted and leaves a . in the leftmost position. For example, 33.25, then 33 is deleted
        $('#minkowski_coef').keyup(function(eve) {
        if ($(this).val().indexOf('.') == 0) {
            console.log("Bailando de caballito");
        }
        });

    });

});