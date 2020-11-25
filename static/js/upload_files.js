$(document).ready(function () {

    $("#upload-file-btn").click(function(){
        console.log("Se quiere subir un archivo");
        var form_data = new FormData($('#upload-file')[0]);
        form_data.append("support",$('#support')[0].value);
        form_data.append("confidence",$('#confidence')[0].value);
        form_data.append("lift",$('#lift')[0].value);
        $("#js-loader").css("display","block")
        //setTimeout(function(){ },3000);
        $.ajax({
            url: '/apriori_process',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                var HTML = response["html"]
                $("#rules_container").html(HTML)
                $("#js-loader").css("display","none");
                console.log(HTML);
            },
            error: function(error){
                $("#js-loader").css("display","none");
                console.log(error);
            }
        });
    });
    
});