$(document).ready(function () {

    if ($('input[type=file]')[0].files.length){
        $(".custom-file-label").html($('input[type=file]')[0].files[0].name);
    }

    change_model_inference($("#models").val());
 
    function change_model_inference(value){
        var form = new FormData();
        form.append("model_name", value);
        $.ajax({
            url: '/change_model_inference',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#vargroup1").html(response["vargroup1"]);
                $("#vargroup2").html(response["vargroup2"]);
                $("#manual_output").html(response["output"]);
                $("#table-output").html("");
            },
            error: function(error){
                set_modal(error);
            }
        });       
    }

    $('#delete-model').on('click', function (e) {
        //$("#warning-modal").removeClass('hide');
        $("#model_name_span").text($("#models").val());
        $('#warning-modal').modal('toggle');
    });

    $('#remove_model_btn').on('click', function (e) {
        var model_name = $("#models").val();
        var form = new FormData();
        form.append("model_name", model_name);
        $.ajax({
            url: '/delete_model',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                location.reload();
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        }); 
    });
    
    $('#models').on('change', function() {
        change_model_inference(this.value);     
    });

    $('#manual-form').on('submit', function (e) {
        e.preventDefault()
        var formData = new FormData(this);
        for (var i = 0; i < this.length - 2; i++) {
            formData.append(this[i].id,this[i].value);
        }  
        $.ajax({
            url: '/inference_model',
            data: formData,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#" + response["output_id"]).val(response["result"]);
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        }); 
    });

    $('#inference-file-btn').on('click', function (e) {
        var form_data = new FormData($('#file-form')[0]);
        $.ajax({
            url: '/file_inference_model',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#table-output").html(response["result"]);
                $('#' + response["table_id"]).DataTable();
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        }); 
    });

    $('#file').on('change',function(e){
        //get the file name
        var fileName = e.target.files[0].name;
        //replace the "Choose a file" label
        $(this).next('.custom-file-label').html(fileName);
    })

    function set_modal(error){
        $("#modal_title").text(error.responseJSON["name"]);
        $("#modal_content").text(error.responseJSON["description"]);
        $('#info-modal').modal('show');
    };

});