var sendBack = null;
var sendBacKSecReq = null;


function textToEvaluate(textEval, bodyText) {
    //console.log(textEval,bodyText);
    $.ajax({
        url: "http://localhost:5000/api/rewrite",
        type: "POST",
        cache: false,
        async: false,
        contentType: "application/json",
        data: JSON.stringify({
            "text": textEval,
            "bodyText": bodyText
        }),
        success: function(result) {
            console.log(result);
            sendBack = result;

        },
        error: function(error) {
            // console.log(error);
        }
    });
}

function getWordExplanation(wordToExplain) {
    console.log(wordToExplain);
    $.ajax({
        url: "http://localhost:5000/api/scraper",
        type: "POST",
        cache: false,
        async: false,
        contentType: "application/json",
        data: JSON.stringify({
            "word": wordToExplain,
            "type": 2
        }),
        success: function(result) {
            console.log(result);
            sendBacKSecReq = result;

        },
        error: function(error) {
            // console.log(error);
        }
    });
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.type == 1) {
            textToEvaluate(request.data, request.all_body);
            sendResponse({ farewell: "goodbye", data: sendBack });
        } else if (request.type == 2) {
            console.log(request.data);
            getWordExplanation(request.data);
            sendResponse({ farewell: "goodbye", data: sendBacKSecReq });
        }
    });

var switchStatus = false;
$("#wordDetectCheckbox").on('change', function() {
    if (!$(this).is(':checked')) {
        switchStatus = $(this).is(':checked');
        //console.log(switchStatus);// To verify

    } else {
        switchStatus = $(this).is(':checked');
        console.log(switchStatus, "true");
        chrome.runtime.onMessage.addListener(
            function(request, sender, sendResponse) {
                if (request.type == 1) {
                    textToEvaluate(request.data, request.all_body);
                    sendResponse({ farewell: "goodbye", data: sendBack });
                } else if (request.type == 2) {

                    getWordExplanation(request.data);
                    sendResponse({ farewell: "goodbye", data: sendBacKSecReq });
                }
            });
    }
});