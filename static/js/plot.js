$(document).ready(function () {
    $("#plot_vars").click(function(){
        var form = new FormData();
        console.log($("#var_abscisa").val());
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
                $("#js-loader").css("display","none");
                console.log(error);
            }
        });  
    });
     
});