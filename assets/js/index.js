$(function() {
    let selected_account = null;
    let date_from = null;
    let date_to = null;
    let country = null;
    let error_message = null;

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

    $('#date-to-input').on('input', function(){    
        if ($(this).val() != '') {
            date_to = $(this).val();
        } 
    });    

    $('#country-input').on('change', function(){    
        country = $(this).val();
    });

    $('.get-data-button').on('click', function(){
        url= $(this).attr('data-url');

        if (!selected_account) {
            alert("Account not selected");
            return;
        }

        $("#results").html('')

        let data = {'account_id': selected_account}

        if ($(this).attr('id') == 'button-transactions') {
            data['date_from'] = date_from;
            data['date_to'] = date_to;
            data['country'] = country;
        }

        $.ajax({
        type: 'GET',
        url : url,
        data : data,
        success: function(data){
            if (data.transactions) {
                displayTransactions(data.transactions);
            }

            if (data.balances) {
                displayBalances(data.balances);
            }

            if (data.account) {
                displayDetails(data.account);
            }

            if (data.error) {
                error_message = data.error
                displayErrorMessage(error_message);
            }
        },
        error: function(data){
            error_message = 'Something went wrong during the request'
            displayErrorMessage(error_message);
        }
        });

        function displayTransactions(data) {
            var event_data = '';
            
            $.each(data, function(key, dataType){
                $.each(dataType, function(index, value){
                    event_data += '<tr>';
                    event_data += '<td>'+index+'</td>';
                    event_data += '<td>'+value.bookingDate+'</td>';
                    event_data += '<td>'+value.transactionAmount.amount+' '+value.transactionAmount.currency+'</td>';
                    event_data += '<td>'+value.remittanceInformationUnstructured+'</td>';
                    event_data += '</tr>';
                });

                $("#results").append(
                    '<h5>Account '+key+' transactions</h5>'+
                    '<table id="table-transactions-'+key+'" class="table table-striped table-hover">'+
                        '<thead class="table-light">'+
                            '<tr>'+
                                '<td class="font-weight-bold">ID</td>'+
                                '<td class="font-weight-bold">Date</td>'+
                                '<td class="font-weight-bold">Amount</td>'+
                                '<td class="font-weight-bold">Details</td>'+
                            '</tr>'+
                        '</thead>'+
                        '<tbody id="table-body-transactions-'+key+'">'+event_data+'</tbody>'+
                    '</table>'
                );
            });
        }

        function displayBalances(data) {
            var event_data = '';

            $.each(data, function(index, value){
                event_data += '<tr>';
                event_data += '<td>'+index+'</td>';
                event_data += '<td>'+value.balanceAmount.amount+' '+value.balanceAmount.currency+'</td>';
                event_data += '<td>'+value.balanceType+'</td>';
                event_data += '<td>'+value.referenceDate+'</td>';
                event_data += '</tr>';
            });

            $("#results").html(
                '<h5>Account balances</h5>'+
                '<table id="table-balances" class="table table-striped table-hover">'+
                    '<thead class="table-light">'+
                        '<tr>'+
                            '<td class="font-weight-bold">ID</td>'+
                            '<td class="font-weight-bold">Balance</td>'+
                            '<td class="font-weight-bold">Type</td>'+
                            '<td class="font-weight-bold">Date</td>'+
                        '</tr>'+
                    '</thead>'+
                    '<tbody id="table-body-balances">'+event_data+'</tbody>'+
                '</table>'
            );
        }

        function displayDetails(data) {
            var event_data = '';
        
            event_data += '<tr><td>Cash account type:</td><td>'+data.cashAccountType+'</td></tr>';
            event_data += '<tr><td>Currency:</td><td>'+data.currency+'</td></tr>';
            event_data += '<tr><td>Iban:</td><td>'+data.iban+'</td></tr>';
            event_data += '<tr><td>Name:</td><td>'+data.name+'</td></tr>';
            event_data += '<tr><td>Product:</td><td>'+data.product+'</td></tr>';
            event_data += '<tr><td>Resource Id:</td><td>'+data.resourceId+'</td></tr>';

            $("#results").html(
                '<h5>Account details</h5>'+
                '<table id="table-balances" class="table table-striped table-hover">'+
                    '<tbody id="table-body-details">'+event_data+'</tbody>'+
                '</table>'
            );
        }

        function displayErrorMessage(error_message) {
            $("#results").html(
                '<h5>Error</h5>'+
                '<div class="font-weight-bold danger">'+error_message+'</div>'
            )
        }

        return false;
    });

});