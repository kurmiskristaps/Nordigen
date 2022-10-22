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

eval("let selected_account = null;\nlet date_from = null;\nlet date_to = null;\nlet country = null;\n\n$(function() {\n    $('.datepickers').datetimepicker({\n        viewMode: 'days',\n        format: 'DD/MM/YYYY'\n    });\n\n    $('#account-selector').on('change', function(){    \n        selected_account = $(this).val();\n    });\n\n    $('#date_from').on('change', function(){    \n        date_from = $(this).val({\n            format: 'DD/MM/YYYY'\n        });\n    });    \n\n    $('#date_to').on('change', function(){    \n        date_to = $(this).val();\n    });    \n\n    $('#country-input').on('change', function(){    \n        country = $(this).val();\n    });\n\n    $('.get-data-button').on('click', function(){\n        url= $(this).attr('data-url');\n\n        if(!selected_account) {\n            alert(\"Account not selected\");\n            return;\n        }\n\n        $.ajax({\n        type: 'GET',\n        url : url,\n        data : {\n            'account_id': selected_account,\n            'date_from': date_from,\n            'date_to': date_to,\n            'country': country,\n        },\n        success: function(data){\n            console.log(\"SUCCESS\")\n            console.log(data)\n        },\n        error: function(data){\n            console.log(\"ERROR\")\n            console.log(data)\n        }\n        });\n\n            return false;\n    });\n});\n\n\n//# sourceURL=webpack:///./assets/js/index.js?");

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