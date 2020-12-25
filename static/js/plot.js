$(document).ready(function () {
    $("#plot_vars").click(function(){
        var form = new FormData();
        //console.log($("#var_abscisa").val());
        form.append("abcisa",$("#var_abscisa").val());
        form.append("ordenada",$("#var_neat").val());
        $.ajax({
            url: '/plot_graph',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#graph_container").html(response["plot"]);
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
     
});