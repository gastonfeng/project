function startTime() {
    var today = new Date();
    var d = today.getDate();
    var M = today.getMonth();
    var y = today.getFullYear();
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

        var page_count = parseInt($("#page_count").text());
        var display_delay = parseInt($("#display_delay").text());

        // Get first page
        delay(function(){
            ajax.jsonRpc("/smartdisplay/getdisplay/", 'call', {
                'display_id': display_id,
            }).then(function (data_display) {
                if(data_display){
                    // Set the count
                    page_count = parseInt(data_display['page_count']);
                    $("#page_count").text(page_count);

                    // Set the delay
                    $("#display_delay").text(parseInt(data_display['display_delay']));

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

        setInterval(function() { counter() }, display_delay * 1000); // Multiplied by 1000 because this method wants microseconds and we manage seconds

        function counter() {
            var index = parseInt($("#page_index").text());

            // Get page for index
            ajax.jsonRpc("/smartdisplay/getnextpage/", 'call', {
                'display_id': display_id,
                'index': index,
            }).then(function (data_page) {
                if(data_page){
                    // Set the count
                    page_count = parseInt(data_page['display_page_count']);
                    $("#page_count").text(page_count);

                    // If iframe, set the frame
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