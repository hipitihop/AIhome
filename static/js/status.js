/**
 * File: /Users/gregbail/AIhome2/static/js/status.js
 * Project: Snips Web Admin
 * Created Date: Friday, March 15th 2019, 10:11:50 pm
 * Author: Greg
 * -----
 * Last Modified: Fri Mar 15 2019
 * Modified By: Greg
 * -----
 * Copyright (c) 2019 Your Company
 * ------------------------------------
 * Javascript will save your soul!
 */


$(document).ready(function () {
    "use strict";
    
    function get_status() {
        $.getJSON("api/services/", function(data) {

            //remove all classes
            $("#status_hotword").removeClass("badge-danger");
            $("#status_nlu").removeClass("badge-danger");
            $("#status_dialogue").removeClass("badge-danger");
            $("#status_asr").removeClass("badge-danger");
            $("#status_tts").removeClass("badge-danger");
            $("#status_skillsserver").removeClass("badge-danger");
            $("#status_audioserver").removeClass("badge-danger");

            $("#status_hotword").removeClass("badge-active");
            $("#status_nlu").removeClass("badge-active");
            $("#status_dialogue").removeClass("badge-active");
            $("#status_asr").removeClass("badge-active");
            $("#status_tts").removeClass("badge-active");
            $("#status_skillsserver").removeClass("badge-active");
            $("#status_audioserver").removeClass("badge-active");


            console.log(data);
            console.log(data !== undefined);
            if (data !== undefined) {
                if ( data['hotword'] != null && data['hotword'] !== undefined) { 
                    if (data['hotword'] == 0) {
                        $("#status_hotword").addClass("badge-danger");
                    } else {
                        $("#status_hotword").addClass("badge-active");
                    }
                }
                else {
                    $("#status_hotword").addClass("badge-danger");
                }
                if ( data['nlu'] != null && data['nlu'] !== undefined) { 
                    if (data['nlu'] == 0) {
                        $("#status_nlu").addClass("badge-danger");
                    } else {
                        $("#status_nlu").addClass("badge-active");
                    }
                }
                else {
                    $("#status_nlu").addClass("badge-danger");
                }
                if ( data['asr'] != null && data['asr'] !== undefined) { 
                    if (data['asr'] == 0) {
                        $("#status_asr").addClass("badge-danger");
                    } else {
                        $("#status_asr").addClass("badge-active");
                    }
                }
                else {
                    $("#status_asr").addClass("badge-danger");
                }
                if ( data['tts'] != null && data['tts'] !== undefined) { 
                    if (data['tts'] == 0) {
                        $("#status_tts").addClass("badge-danger");
                    } else {
                        $("#status_tts").addClass("badge-active");
                    }
                }
                else {
                    $("#status_tts").addClass("badge-danger");
                }
                if ( data['dialogue'] != null && data['dialogue'] !== undefined) { 
                    if (data['dialogue'] == 0) {
                        $("#status_dialogue").addClass("badge-danger");
                    } else {
                        $("#status_dialogue").addClass("badge-active");
                    }
                }
                else {
                    $("#status_dialogue").addClass("badge-danger");
                }
                if ( data['skillserver'] != null && data['skillserver'] !== undefined) { 
                    if (data['skillserver'] == 0) {
                        $("#status_skillsserver").addClass("badge-danger");
                    } else {
                        $("#status_skillsserver").addClass("badge-active");
                    }
                }
                else {
                    $("#status_skillsserver").addClass("badge-danger");
                }
                if ( data['audioserver'] != null && data['audioserver'] !== undefined) { 
                    if (data['audioserver'] == 0) {
                        $("#status_audioserver").addClass("badge-danger");
                    } else {
                        $("#status_audioserver").addClass("badge-active");
                    }
                }
                else {
                    $("#status_audioserver").addClass("badge-danger");
                }
            }

        });
    }



    $('a[data-toggle="dropdown"]').parent().on('show.bs.dropdown', function(e) {
        get_status();
    })

    
});


