visualization_method
$(document).ready(function () {
    $("#visualization_method").click(function(){
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/get_visualization_method',
            type: 'GET',
            contentType: false,
            processData: false,
            success: function(response){
                $("#heatmap").html(response["heatmap_html"]);
            },
            error: function(error){
                console.log(error);
            }
        });  
        $("#js-loader").css("display","none");
    });
});