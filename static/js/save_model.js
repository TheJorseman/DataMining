

$(document).ready(function () {


    $("#save-linear-model-btn").on("click", function(e){
        e.stopImmediatePropagation();
        save_model($("#model_name_linear").val(), '#show_linear_inference_link');
    });

    $("#save-log-model-btn").on("click", function(e){
        e.stopImmediatePropagation();
        console.log($("#model_log_name").val());
        save_model($("#model_log_name").val(), '#show_log_inference_link'); 
    });


    function save_model(name, id_show) {
        var form = new FormData();
        if (name == ""){
            $("#modal_title").text("Error");
            $("#modal_content").text("Debe de Escribir un nombre para el modelo");
            $('#info-modal').modal('show');
            return 
        }
        form.append("model_name",name);
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/save_model',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#modal_title").text(response["title"]);
                $("#modal_content").text(response["content"]);
                $('#info-modal').modal('show');
                $(id_show).css("display","block");
                $("#js-loader").css("display","none");
                return true
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
                return false
            }
        }); 
    };

    function set_modal(error){
        $("#modal_title").text(error.responseJSON["name"]);
        $("#modal_content").text(error.responseJSON["description"]);
        $('#info-modal').modal('show');
    };

});