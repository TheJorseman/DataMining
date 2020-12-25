$(document).ready(function () {
    
    if ($('#clustering_method')[0].value == "partitional"){
        $("#heuristic_container").css("display","block");
    }else{
        $("#heuristic_container").css("display","none");
    }

    $("#clustering_button").click(function(){
        var form = new FormData();
        form.append("method",$("#clustering_method").val());
        form.append("n_clusters",$("#n_clusters").val());
        $("#js-loader").css("display","block");
        console.log(form);
        $.ajax({
            url: '/clustering_process',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#clustering_container").html(response["clustering_summary"]);
                $("#export").css("display","block");
                //clustering_table
                $('#clustering_table').DataTable();
                $("#js-loader").css("display","none");
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        });  
    });


    $("#visualization_method").click(function(){
        var form = new FormData();
        form.append("method",$("#clustering_method").val());
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/get_visualization_method',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#visualization_method_container").html(response["visualization_html"]);
                $("#js-loader").css("display","none");
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        });  
    });

    $("#heuristic_method").click(function(){
        $("#js-loader").css("display","block");
        var form = new FormData();
        form.append("method",$("#clustering_method").val());
        $.ajax({
            url: '/get_heuristic_method',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#n_clusters").val(response["elbow"]);
                $("#span_elbow").text(response["elbow"]);
                $("#elbow_container").css("display","block");
                $("#js-loader").css("display","none");
                
            },
            error: function(error){
                set_modal(error);
                $("#js-loader").css("display","none");
            }
        });  
        
    });

    $('#clustering_method').on('change', function() {
        if (this.value == "partitional"){
            $("#heuristic_container").css("display","block");
        }else{
            $("#heuristic_container").css("display","none");
        }
    });

    $("#n_clusters").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
           //display error message
           $("#errmsgs").html("Solo se admiten digitos").show().fadeOut("slow");
                  return false;
       }
    });


    function set_modal(error){
        $("#modal_title").text(error.responseJSON["name"]);
        $("#modal_content").text(error.responseJSON["description"]);
        $('#info-modal').modal('show');
    };

});