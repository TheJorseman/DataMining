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


    $('#var-sel-collaps-linear').one('show.bs.collapse', function (e) {
        //$("#js-loader").css("display","block");
        e.preventDefault()
        $.ajax({
            url: '/get_regression_vars',
            type: 'GET',
            contentType: false,
            processData: false,
            success: function(response){
                $("#input-var-lin-reg").html(response["colum-sel"]);
                $("#table-input-reg").attr("id", "table-input-lin-reg");
                $("#output-var-lin-reg").html(response["options"]);
                $("#js-loader").css("display","none");
                $('#var-sel-collaps-linear').collapse('show');
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        });  

    });

    $('#train-linear-regression').on('click', function () {
        var form = new FormData();
        //form.append("input",$("#output-var-reg").val());
        var output_var_number = 0;
        if (!$('#table-input-lin-reg').length){
            form.append("input","all");
            form.append("output","first");
            output_var_number += 1
        }else{
            $('#table-input-lin-reg tr').each(function () {
                $(this).find('td input:checked').each(function () {
                    form.append(this.name,true);
                    output_var_number += 1;
                });
            });
            form.append("output",$("#output-var-lin-reg").val());
        }
        if (output_var_number == 0){
            $("#modal_title").text("Error");
            $("#modal_content").text("Debe SELECCIONAR al menos UNA variable de ENTRADA");
            $('#info-modal').modal('show');
            return 
        }
        //$("#js-loader").css("display","block");
        $.ajax({
            url: '/linear_regression',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                //console.log(response);
                $("#linear-model-data").html("<h5>Resultados</h5>"+response["html_join"]);
                $("#input-ordenada").html(response["colum-sel"]);
                $("#input-abscisa").html(response["options"]);
                $("#plot_regression").css("display","block");
                $("#save-linear #save_model").css("display","block");
                $("#js-loader").css("display","none");
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        }); 
    });

    $('#plot-regression').on('click', function () {
        var form = new FormData();
        var output_var_number = 0;
        $('#table-x-reg tr').each(function () {
            $(this).find('td input:checked').each(function () {
                form.append(this.name,true);
                output_var_number += 1;
            });
        });
        form.append("output",$("#input-abscisa").val());
        if (output_var_number == 0){
            $("#modal_title").text("Error");
            $("#modal_content").text("Debe SELECCIONAR al menos UNA variable de ENTRADA");
            $('#info-modal').modal('show');
            return 
        }
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/plot_regression',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#graph_container").html(response["image"]);
                $("#js-loader").css("display","none");
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        }); 
    });


    $('#train-log-regression').on('click', function () {
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
        //$("#js-loader").css("display","block");
        $.ajax({
            url: '/logistic_regression',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                //$("#graph_container").html(response["plot"]);
                $("#logistic-metrics").html(response["html-join"]);
                $("#logistic_save #save_model").css("display","block");
                $("#js-loader").css("display","none");
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