$(document).ready(function () {

    $("#upload-file-btn").click(function(){
        console.log("Se quiere subir un archivo");
        var form_data = new FormData($('#upload-file')[0]);
        form_data.append("support",$('#support')[0].value);
        form_data.append("confidence",$('#confidence')[0].value);
        form_data.append("lift",$('#lift')[0].value);
        $("#js-loader").css("display","block");
        //setTimeout(function(){ },3000);
        $.ajax({
            url: '/apriori_process',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                var HTML = response["html"];
                $("#rules_container").html(HTML);
                $("#js-loader").css("display","none");
                console.log(HTML);
            },
            error: function(error){
                $("#js-loader").css("display","none");
                console.log(error);
            }
        });
    });

    var columns;

    $("#analize-file-btn").click(function(){
        var form_data = new FormData($('#analize-file-form')[0]);
        $.ajax({
            url: '/analize_data',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features").html(response["sel_columns_html"]);
                $("#span_len").text(response["df_len"]);
                $("#df_len").val(response["df_len"]);
                $("#head_table").html(response["head"]);
                columns = response["columns"];
                $("#features-container").css("display","block");
                $("#js-loader").css("display","none");
                //console.log(response);
            },
            error: function(error){
                $("#js-loader").css("display","none");
                console.log(error);
            }
        });    
    });


    $("#save-conf-btn").click(function(){
        var conf_form = new FormData($('#config-data-form')[0]);
        conf_form.append("len",$("#df_len")[0].value);
        conf_form.append("random",$("#random")[0].value);
        columns.forEach(column => {
            var iid = "#" + column
            if ($(iid).length){
                conf_form.append(column,$(iid)[0].checked);
            }
        });
        $.ajax({
            url: '/save_conf',
            data: conf_form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#base").css("display","none");
                $("#algorithm").css("display","block");
                $("#filename_summary").text(response["filename"]);
                $("#rows_summary").text(response["df_len"]);
                $("#table_summary").html(response["sel_columns_html"]);
                scrollToTop();
                //Load inmeddiatly the correlation data
                if ($("#correlation").length) { 
                    correlation();
                }
            },
            error: function(error){
                $("#js-loader").css("display","none");
                console.log(error);
            }
        });  
    });

    function scrollToTop() { 
        window.scrollTo(0, 0); 
    }; 



    function correlation(){
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/correlation_process',
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                //console.log(response);
                $("#pearson_correlation_matrix").html(response["correlation_matrix_html"]);
                $("#heatmap").html(response["heatmap_html"]);
                $("#var_abscisa").html(response["options"]);
                $("#var_neat").html(response["options"]);
                $("#js-loader").css("display","none");
            },
            error: function(error){
                //$("#js-loader").css("display","none");
                console.log(error);
            }
        });     
    };
});