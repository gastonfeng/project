function startTime() {
    var today = new Date();
    var d = today.getDate();
    var M = today.getMonth();
    var y = today.getYear();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('date_time_clock').innerHTML = d + "/" + M + "/" + y + " " + h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
}

function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}

var delay = ( function() {
    var timer = 0;
    return function(callback, ms) {
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();

function startPageManager() {
    odoo.define('project_smart_display.smart_display_viewing', ['web.ajax'], function (require) {
        "use strict";
        var ajax = require('web.ajax');

        var display_id = parseInt($("#display_id").text());

        var page_count = parseInt($("#page_count").text()); // TODO replace this by a JSON REQUEST

        // Get first page
        delay(function(){
            ajax.jsonRpc("/smartdisplay/getdisplay/", 'call', {
                'display_id': display_id,
            }).then(function (data_display) {
                if(data_display){
                    ajax.jsonRpc("/smartdisplay/getnextpage/", 'call', {
                        'display_id': data_display['display_id'],
                        'index': 0,
                    }).then(function (data_page) {
                        if(data_page){
                            if (data_page['mode'] == 'iframe') {
                                document.getElementById('page_iframe').setAttribute('src', data_page['iframe_url']);
                                document.getElementById('page_iframe').style.display = "inline";
                            }
                        }
                    })
                }
            })
        });

        setInterval(function() { counter() }, 30000); // And wait 30s TODO : set this param dynamically

        function counter() {
            var index = parseInt($("#page_index").text());

            // Get page for index
            ajax.jsonRpc("/smartdisplay/getnextpage/", 'call', {
                'display_id': display_id,
                'index': index,
            }).then(function (data_page) {
                if(data_page){
                    if (data_page['mode'] == 'iframe') {
                        document.getElementById('page_iframe').setAttribute('src', data_page['iframe_url']);
                        document.getElementById('page_iframe').style.display = "inline";
                    }
                }
            })

            // Increase index
            if (index < page_count) {
                index = index + 1;
            }
            else {
                index = 1;
            }
            $("#page_index").text(index);

        }
    });
}