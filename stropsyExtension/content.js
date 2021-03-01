/*
let getParagraphs=document.getElementsByTagName("p");

let sumUp=""
for( var i=0;i<getParagraphs.length;i++){
    sumUp+=getParagraphs[i].outerText;
}
*/
/*
let getParagraphs=document.getElementsByTagName("p");
var getBody=[];


for( var i=0;i<4;i++){
    getBody.push(getParagraphs[i].innerHTML);
}

var bodyText=$('body').html();

chrome.runtime.sendMessage({"type": 1,"data":getBody,"all_body":bodyText}, function(response) {
    console.log(response.data);
    var re = new RegExp("\\w+");
    var save;
    for( var i=0;i<4;i++){
        save=re.test(response.data[i][0]);
        
            getParagraphs[i].innerHTML=getParagraphs[i].textContent.replace(/response.data[i][0]/gi,"sdfdsfsd");
        
        //getParagraphs[i].innerHTML=response.data[i];
       // console.log([getParagraphs[i].innerHTML,response.data[i]]);
    }
   // $("body").html();
    
  });

  $(document).on("click", function(event){
    //var getData=$(event.target.dataset.idGet).html();
    //console.log(getData.length,getData);
    
    if(event.target.className=="tooltip detect-text" ){
        //if(getData.length<30){
            chrome.runtime.sendMessage({"type": 2,"data":event.target.outerText+" "+document.title}, function(response) {
                console.log(response);
                $(event.target.dataset.idGet).append("<br/>"+response.data);
            });
        //}
    }
})
https://en.wikipedia.org/wiki/Emperor_of_China -660
 https://freestyleacademy.rocks/Digital_Media/examples/index.php?f=Mouse_Following_Div_On_Hover
*/



let getParagraphs = document.getElementsByTagName("p");
var getBody = [];


for (var i = 0; i < 4; i++) {
    getBody.push(getParagraphs[i].innerHTML);
}

var bodyText = $('body').html();

document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement,
        text = target.textContent || target.innerText;
}, false);


chrome.runtime.sendMessage({ "type": 1, "data": getBody, "all_body": bodyText }, function(response) {
    console.log(response);

    var context = document.querySelectorAll("p");

    console.log(response.data.length);
    if (response.data.length < 700) {
        for (var i = 0; i < getParagraphs.length; i++) {
            var instance = new Mark(context[i]);
            for (var j = 0; j < response.data.length; j++) {
                instance.mark(response.data[j][0], {
                    "separateWordSearch": false,
                    "acrossElements": true,
                    accuracy: "exactly",
                    element: "stropsy",
                    className: "stropsy-element-" + j
                });
            }
        }
    } else {
        for (var i = 0; i < 4; i++) {
            var instance = new Mark(context[i]);
            for (var j = 0; j < response.data.length; j++) {
                instance.mark(response.data[j][0], {
                    "separateWordSearch": false,
                    "acrossElements": true,
                    accuracy: "exactly",
                    element: "stropsy",
                    className: "stropsy-element-" + j
                });
            }
        }
    }





});


var btn = document.createElement("stropsy-popup");
btn.innerHTML = ` <div class="content-stropsy all-stropsy-content-from-popup">
  <div class="title_stropsy all-stropsy-content-from-popup" id="stropsy-3edwwx" style="font-family: sans-serif !important;font-size: 26px !important;"></div>
  <div class="stropsy-desc-word all-stropsy-content-from-popup" id="stropsy-d2ex2a1223" style="
  font-family: sans-serif !important;
  font-size: 16px !important;
  color: #444 !important;
  font-weight: 400 !important ;
  letter-spacing: -.013em !important;
  line-height: 1.43 !important;"></div>
  </div>`;
//document.body.appendChild(btn);
//btn.style.display = "none";
//https://api.dictionaryapi.dev/api/v2/entries/en_US/aglutinogen
//https: //stackoverflow.com/questions/33863807/youtube-data-api-v3-using-javascript
$(document).on("click", function(event) {
    //var getData=$(event.target.dataset.idGet).html();
    console.log(event);

    if (event.target.nodeName == "STROPSY" || event.target.nodeName == "STROPSY-POPUP") {
        if (event.target.nodeName == "STROPSY") {
            $("stropsy-popup").remove();
            event.target.innerHTML = event.target.innerHTML + "<stropsy-popup>" + btn.innerHTML + "</stropsy-popup>";

            btn.style.display = "inline";
            $(".title_stropsy").html("<div class='image_read-stropsy all-stropsy-content-from-popup'></div>" + event.target.innerText);



            chrome.runtime.sendMessage({ "type": 2, "data": event.target.outerText + " site:wikipedia.org" }, function(response) {
                console.log(response, response.data.items[0].pagemap.cse_image[0].src);

                $("#stropsy-d2ex2a1223").html(response.data.items[0].snippet + `<a href='" + response.data.items[0].link + "'>read more</a><br/>
                <ul class="tiles_pages all-stropsy-content-from-popup" style="list-style-type:none;list-style-image:none;display: inline-flex;">
                <li class="list-tiles all-stropsy-content-from-popup" style="margin-right: 12px;" onclick="accesTab(1)">Pages</li>
                <li class="list-tiles  all-stropsy-content-from-popup" style="margin-right: 12px;" onclick="accesTab(2)">Images</li>
                <li class="list-tiles  all-stropsy-content-from-popup" style="margin-right: 12px;" onclick="accesTab(3)">Videos</li>
                <li class="list-tiles  all-stropsy-content-from-popup" style="margin-right: 12px;" onclick="accesTab(4)">News</li>
                <li class="list-tiles all-stropsy-content-from-popup" style="margin-right: 12px;" onclick="accesTab(5)">Tweetes</li>
                </ul>
                <div class="content-display-data  all-stropsy-content-from-popup"> <ul class='add-data-to-href  all-stropsy-content-from-popup'></ul></div>
               
         `);
                for (var i = 1; i < response.data.items.length; i++) {
                    $(".add-data-to-href").append("<li class='link-popup' style='margin-bottom:0px!important;'><a href='" + response.data.items[i].link + "'>" + response.data.items[i].htmlTitle + "</a></li>");
                }
                $(".image_read-stropsy").html("<img src='" + response.data.items[0].pagemap.cse_image[0].src + "' width='100%' height='200px'/>");
            });

        }
    } else {
        if (event.target.nodeName != "STROPSY-POPUP") {
            if (event.target.classList[1] != "all-stropsy-content-from-popup") {
                $("stropsy-popup").remove();
            }
        }
    }
})