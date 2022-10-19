let selected_account = null;

$(function() {
    $('#account-selector').on('change', function(){    
        selected_account = $(this).val();
    });

    $('.get-data-button').on('click', function(){
        url= $(this).attr('data-url');

        if(!selected_account) {
            alert("Account not selected");
            return;
        }

        $.ajax({
        type: 'GET',
        url : url,
        data : {'account_id': selected_account},
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
