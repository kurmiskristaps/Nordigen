/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/js/index.js":
/*!****************************!*\
  !*** ./assets/js/index.js ***!
  \****************************/
/***/ (() => {

eval("$(function() {\n    let selected_account = null;\n    let date_from = null;\n    let date_to = null;\n    let country = null;\n    let error_message = 'Something went wrong during the request';\n\n    $('.form-selector').on('change', function(){    \n        selected_account = $(this).val();\n    });\n\n    $('.datepickers').datetimepicker({\n        viewMode: 'days',\n        format: 'YYYY-MM-DD'\n    });\n\n    $('#date-from-input').on('input', function(){ \n        if ($(this).val() != '') {\n            date_from = $(this).val();\n        }   \n    });    \n\n    $('#date-to-input').on('input', function(){    \n        if ($(this).val() != '') {\n            date_to = $(this).val();\n        } \n    });    \n\n    $('#country-input').on('change', function(){    \n        country = $(this).val();\n    });\n\n    $('.get-data-button').on('click', function(){\n        url= $(this).attr('data-url');\n\n        if (!selected_account) {\n            alert(\"Account not selected\");\n            return;\n        }\n\n        $(\"#results\").html('');\n        $(\"#loading\").removeClass('d-none');\n        $('#accpunt-form :input').attr('disabled', true);\n\n        let data = {'account_id': selected_account};\n\n        if ($(this).attr('id') == 'button-transactions') {\n            data['date_from'] = date_from;\n            data['date_to'] = date_to;\n            data['country'] = country;\n        }\n\n        $.ajax({\n        type: 'GET',\n        url : url,\n        data : data,\n        success: function(data){\n            if (data.transactions) {\n                displayTransactions(data.transactions);\n            }\n\n            if (data.balances) {\n                displayBalances(data.balances);\n            }\n\n            if (data.account) {\n                displayDetails(data.account);\n            }\n\n            if (data.error) {\n                displayErrorMessage(data.error);\n            }\n\n            if (data.status_code >= 400) {\n                let message = Object.values(data)[0];\n                message = message.summary ?? Object.values(message)[0];\n                message = message ?? error_message;\n                \n                displayErrorMessage(message);\n            }\n        },\n        error: function(data){\n            displayErrorMessage(error_message);\n        }\n        });\n\n        function displayTransactions(data) {\n            let html = '';\n            \n            $.each(data, function(key, dataType){\n                var event_data = '';\n                \n                $.each(dataType, function(index, value){\n                    let date = '';\n\n                    if (value.bookingDate) {\n                        date = value.bookingDate;\n                    } else if (value.valueDate) {\n                        date = value.valueDate\n                    }\n\n                    event_data += '<tr>';\n                    event_data += '<td>'+index+'</td>';\n                    event_data += '<td>'+date+'</td>';\n                    event_data += '<td>'+value.transactionAmount.amount+' '+value.transactionAmount.currency+'</td>';\n                    event_data += '<td>'+value.remittanceInformationUnstructured+'</td>';\n                    event_data += '</tr>';\n                });\n\n                html +=\n                    '<h5>Account '+key+' transactions</h5>'+\n                    '<table id=\"table-transactions-'+key+'\" class=\"table table-striped table-hover\">'+\n                        '<thead class=\"table-light\">'+\n                            '<tr>'+\n                                '<td class=\"font-weight-bold\">ID</td>'+\n                                '<td class=\"font-weight-bold\">Date</td>'+\n                                '<td class=\"font-weight-bold\">Amount</td>'+\n                                '<td class=\"font-weight-bold\">Details</td>'+\n                            '</tr>'+\n                        '</thead>'+\n                        '<tbody id=\"table-body-transactions-'+key+'\">'+event_data+'</tbody>'+\n                    '</table>'\n                ;\n\n            });\n\n            showResults(html);\n        }\n\n        function displayBalances(data) {\n            var event_data = '';\n\n            $.each(data, function(index, value){\n                event_data += '<tr>';\n                event_data += '<td>'+index+'</td>';\n                event_data += '<td>'+value.balanceAmount.amount+' '+value.balanceAmount.currency+'</td>';\n                event_data += '<td>'+value.balanceType+'</td>';\n                event_data += '<td>'+value.referenceDate+'</td>';\n                event_data += '</tr>';\n            });\n\n            $(\"#results\").html(\n                '<h5>Account balances</h5>'+\n                '<table id=\"table-balances\" class=\"table table-striped table-hover\">'+\n                    '<thead class=\"table-light\">'+\n                        '<tr>'+\n                            '<td class=\"font-weight-bold\">ID</td>'+\n                            '<td class=\"font-weight-bold\">Balance</td>'+\n                            '<td class=\"font-weight-bold\">Type</td>'+\n                            '<td class=\"font-weight-bold\">Date</td>'+\n                        '</tr>'+\n                    '</thead>'+\n                    '<tbody id=\"table-body-balances\">'+event_data+'</tbody>'+\n                '</table>'\n            );\n        }\n\n        function displayDetails(data) {\n            var event_data = '';\n        \n            event_data += '<tr><td>Cash account type:</td><td>'+data.cashAccountType+'</td></tr>';\n            event_data += '<tr><td>Currency:</td><td>'+data.currency+'</td></tr>';\n            event_data += '<tr><td>Iban:</td><td>'+data.iban+'</td></tr>';\n            event_data += '<tr><td>Name:</td><td>'+data.name+'</td></tr>';\n            event_data += '<tr><td>Product:</td><td>'+data.product+'</td></tr>';\n            event_data += '<tr><td>Resource Id:</td><td>'+data.resourceId+'</td></tr>';\n\n            $(\"#results\").html(\n                '<h5>Account details</h5>'+\n                '<table id=\"table-balances\" class=\"table table-striped table-hover\">'+\n                    '<tbody id=\"table-body-details\">'+event_data+'</tbody>'+\n                '</table>'\n            );\n        }\n\n        function displayErrorMessage(error_message) {\n            $(\"#results\").html(\n                '<h5>Error</h5>'+\n                '<div class=\"    text-danger\">'+error_message+'</div>'\n            )\n        }\n\n        function showResults(html) {\n            $('#accpunt-form :input').attr('disabled', false);\n            $(\"#loading\").addClass('d-none');\n            $(\"#results\").html(html);\n        }\n\n        return false;\n    });\n\n});\n\n//# sourceURL=webpack:///./assets/js/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/js/index.js"]();
/******/ 	
/******/ })()
;