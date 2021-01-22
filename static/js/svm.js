$(document).ready(function () {


    $('#var-sel-collaps').one('show.bs.collapse', function (e) {
        //$("#js-loader").css("display","block");
        e.preventDefault()
        $.ajax({
            url: '/get_regression_vars',
            type: 'GET',
            contentType: false,
            processData: false,
            success: function(response){
                $("#input-var-reg").html(response["colum-sel"]);
                $("#output-var-reg").html(response["options"]);
                $("#js-loader").css("display","none");
                $('#var-sel-collaps').collapse('show');
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        });  

    });

    $('#train-svm').on('click', function () {
        var form = new FormData();
        //form.append("input",$("#output-var-reg").val());
        var output_var_number = 0;
        if (!$('#table-input-reg').length){
            form.append("input","all");
            form.append("output","first");
            output_var_number += 1
        }else{
            $('#table-input-reg tr').each(function () {
                $(this).find('td input:checked').each(function () {
                    form.append(this.name,true);
                    output_var_number += 1;
                });
            });
            form.append("output",$("#output-var-reg").val());
        }
        if (output_var_number == 0){
            $("#modal_title").text("Error");
            $("#modal_content").text("Debe SELECCIONAR al menos UNA variable de ENTRADA");
            $('#info-modal').modal('show');
            return 
        }
        form.append("train-percent",$("#train-percent-slider")[0].value);
        form.append("kernel",$("#kernel").val());
        
        $.ajax({
            url: '/train_svm',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            beforeSend: function() { $("#js-loader").css("display","block");},
            complete: function() { $("#js-loader").css("display","none");},
            success: function(response){
                //$("#graph_container").html(response["plot"]);
                $("#svm-metrics").html(response["html-join"]);
                $("#svm_save #save_model").css("display","block");
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        }); 
    });

    function set_modal(error){
        $("#modal_title").text(error.responseJSON["name"]);
        $("#modal_content").text(error.responseJSON["description"]);
        $('#info-modal').modal('show');
    };


    $("#train-percent-slider").on("input",function(){
        $("#train-percent-input").val($('#train-percent-slider')[0].value);
        $("#test-percent-input").val(100 - $('#train-percent-slider')[0].value);
    });

});