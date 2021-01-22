$(document).ready(function () {

    var columns;

    $("#show_pearson_matrix").click(function(){
        $("#js-loader").css("display","block");
        $.ajax({
            url: '/pearson_correlation_heatmap',
            type: 'GET',
            contentType: false,
            processData: false,
            success: function(response){
                $("#heatmap").html(response["heatmap_html"]);
            },
            error: function(error){
                set_modal(error);
            }
        });  
        $("#js-loader").css("display","none");
    });


    $("#save-columns-btn").click(function(){
        $("#js-loader").css("display","block");
        var form_data = new FormData();
        if ($("input:visible").length){
            $("input:visible").each(function (i){
                console.log(this.id);
                if(columns.includes(this.id)){
                    form_data.append(this.id,this.checked)
                }
            });
        };
        $.ajax({
            url: '/set_current_columns',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#all-columns-common").prop("checked",true);
                $("#table_summary").html(response["summary_columns"]);
                $("#features-common").css("display","none");
            },
            error: function(error){
                set_modal(error);
            }
        });  
        $("#js-loader").css("display","none");
    });


    $("#all-columns-common").change(function() {
        if(!this.checked) {
            $("#js-loader").css("display","block");
            $.ajax({
                url: '/get_current_columns',
                type: 'GET',
                contentType: false,
                processData: false,
                success: function(response){
                    $("#features-common-container").html(response["sel_columns_html"]);
                    columns = response["columns"];
                    $("#features-common").css("display","block");
                },
                error: function(error){
                    set_modal(error);
                }
            });  
            $("#js-loader").css("display","none");
        }else{
            $("#features-common").css("display","none");
        }
    });


    function set_modal(error){
        $("#modal_title").text(error.responseJSON["name"]);
        $("#modal_content").text(error.responseJSON["description"]);
        $('#info-modal').modal('show');
    };


    $("#button-toggle-sidebar").on('click', function () {
        console.log("Toggle");
        $('#sidebar').toggleClass('active');
    });
});