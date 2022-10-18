let selected_account = null;

$(document).ready(function(){
    $('#account-selector').on('change', function(){    
        selected_account = $(this).val();
    });

    $('.get-data-button').bind('click', function(){
        selected_account= $(this).attr('account-id');
        task_id= $(this).attr('task-id');
        url= $(this).attr('data-url');
            $.ajax({
            type: 'GET',
            url : url,
            data : {'task_id': task_id},
            success: function(data){
                console.log("SUCCESS")
                console.log(data)
            },
            error: function(data){
                console.log("ERROR")
                console.log(data)
            }
            });

            return false;
    });
});
