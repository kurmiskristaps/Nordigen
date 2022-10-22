let selected_account = null;
let date_from = null;
let date_to = null;
let country = null;

$(function() {
    $('#account-selector').on('change', function(){    
        selected_account = $(this).val();
    });

    $('.datepickers').datetimepicker({
        viewMode: 'days',
        format: 'YYYY-MM-DD'
    });

    $('#date-from-input').on('input', function(){ 
        if ($(this).val() != '') {
            date_from = $(this).val();
        }   
    });    

    $('#date-to-input').on('change', function(){    
        if ($(this).val() != '') {
            date_to = $(this).val();
        } 
    });    

    $('#country-input').on('change', function(){    
        country = $(this).val();
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
        data : {
            'account_id': selected_account,
            'date_from': date_from,
            'date_to': date_to,
            'country': country,
        },
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
