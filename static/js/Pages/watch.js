/**
 * File: /Users/gregbail/AIhome2/static/js/Pages/Watch.js
 * Project: Snips Web Admin
 * Created Date: Tuesday, March 12th 2019, 11:44:02 pm
 * Author: Greg
 * -----
 * Last Modified: Sat Mar 16 2019
 * Modified By: Greg
 * -----
 * Copyright (c) 2019 Your Company
 * ------------------------------------
 * Javascript will save your soul!
 */


$(document).ready(function () {
    "use strict";

    //going to get a list of all the sites in the DB
    //then add the sites to the dorpdown to allow for site filters
    var btns = [];
    var siteIDList = []
    var loadingData = false;
    var site = '0';
    var last_date = '2200-01-01'; //this is used to send back to the api to get more records from this date string
    var canLoadMore = true;
    

    $.getJSON("api/sites/", function(data) {
        if (data) {
            
            //load all the different sites from the system into a select box to filter log view
            siteIDList = data;
            btns.push('<option value="0">All Sites</option>');
            for(var i = 0; i < data.length; i++) {
                var item = data[i];
                btns.push('<option value="' + item['id'] + '">' + item['name'] + '</option>');
            }
        }
        $("#timelineSites").html(btns);
    });

    
    function load_rows() {
        //get 50 rows at a time to display
        //if 50 rows are not returned then there are no more records to ask for
        $.getJSON("api/watch/" + site + '/' + last_date, function(data) {
            if (data['last_date'] !== undefined) {
                if (last_date == '2200-01-01' && data['rows'].length == 0) {
                    $("#timelineview").html('<div id="nothingtoshow" class="d-flex justify-content-center"><div>Nothing to show</div></div>');
                }
                else {
                    last_date = data['last_date'];

                    //if LOADING Div there.. remove it
                    $( "#loadingbox" ).remove();

                    //if nothing to show is there.. we remove it
                    $( "#nothingtoshow" ).remove();

                    //if the listing ul control is not there add one
                    if($("#timelinelist").length == 0) {
                        //it doesn't exist
                        $('#timelineview').append('<ul id="timelinelist" class="timeline"></ul>');
                      }

                    for(var i = 0; i < data['rows'].length; i++) {
                        var obj = data['rows'][i];
            
                        var html = '<li class="d-flex timeline-inverted">';

                        switch (obj['hermes']) {
                            case 1:
                                //dialogue manager
                                html += ' <div class="timeline-badge dm"><i class="mdi mdi-36px mdi-sitemap"></i> </div> \
                                    <div class="timeline-panel dm-bg">';
                                break; 
                            case 2:
                                //nlu
                                html += ' <div class="timeline-badge nlu"><i class="mdi mdi-36px mdi-target-variant"></i> </div> \
                                    <div class="timeline-panel nlu-bg">';
                                break; 
                            case 3:
                                //tts
                                html += ' <div class="timeline-badge tts"><i class="mdi mdi-36px mdi-voice"></i> </div> \
                                        <div class="timeline-panel tts-bg">';
                                break; 
                            case 4:
                                //hotwords
                                html += ' <div class="timeline-badge wakeword"><i class="mdi mdi-36px mdi-bullhorn"></i> </div> \
                                        <div class="timeline-panel wakeword-bg">';
                                break; 
                            case 5:
                                //asr
                                html += ' <div class="timeline-badge asr"><i class="mdi mdi-36px mdi-microphone"></i> </div> \
                                        <div class="timeline-panel asr-bg">';
                                break; 
                            case 6:
                                //error
                                html += ' <div class="timeline-badge error"><i class="mdi mdi-36px mdi-alert-circle-outline"></i> </div> \
                                        <div class="timeline-panel error-bg">';
                                break; 
                            case 7:
                                //intents
                                html += ' <div class="timeline-badge intent"><i class="mdi mdi-36px mdi-code-braces"></i> </div> \
                                        <div class="timeline-panel intent-bg">';
                                break; 
                            case 8:
                                //audioserver
                                html += ' <div class="timeline-badge audioserver" ><i class="mdi mdi-36px mdi-volume-high"></i> </div> \
                                        <div class="timeline-panel audioserver-bg">';
                                break; 
                            default: 
                                html += ' <div class="timeline-badge success"><i class=""></i> </div> \
                                        <div class="timeline-panel">';
                        }


                        html += '<div class="d-flex timeline-heading"> \
                                                <div class="flex-grow-1"><h4 class="timeline-title">' + obj['fullhermes'] + ' - ' + obj['hermesTopic'] + '</h4></div> \
                                                <div ><small class="text-muted">' + obj['timestamp'] + '</small></div> \
                                            </div> \
                                            <div class="timeline-body">'
                        //wakeword mofel
                        if ( obj['modelId'] != null && obj['modelId'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Wakeword Model</div><div class="col">' + obj['modelId'] + '</div> \
                                            </div>' }
                        //site info
                        if ( obj['site'] != null && obj['site']['name'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Device</div><div class="col">' + obj['site']['name'] + '</div> \
                                            </div>' }
                        //sessionId
                        if ( obj['sessionId'] != null && obj['sessionId'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Session Id</div><div class="col">' + obj['sessionId'] + '</div> \
                                            </div>' }
                        
                        //startsessiontype
                        if ( obj['startsessiontype'] != null && obj['startsessiontype'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Session Start Type</div><div class="col">' + obj['startsessiontype'] + '</div></div>' }
                        if ( obj['text'] != null && obj['text'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Text</div><div class="col">' + obj['text'] + '</div></div>' 
                        }
                        if ( obj['intentFilter'] != null && obj['intentFilter'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Intent Filter</div><div class="col">' + obj['intentFilter'] + '</div></div>' 
                        }
                        if ( obj['canBeEnqueued'] != null && obj['canBeEnqueued'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Can Be Enqueued</div><div class="col">' + obj['canBeEnqueued'] + '</div></div>' 
                        }
                        if ( obj['sendIntentNotRecognized'] != null && obj['sendIntentNotRecognized'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Send Intent Not Recognized</div><div class="col">' + obj['sendIntentNotRecognized'] + '</div></div>' 
                        }
                                        
                        



                        //reactivatedFromSessionId
                        if ( obj['reactivatedFromSessionId'] != null && obj['reactivatedFromSessionId'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Reactivated From Session Id</div><div class="col">' + obj['reactivatedFromSessionId'] + '</div> \
                                            </div>' }
                        
                        //input
                        if ( obj['intentinput'] != null && obj['intentinput'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Input</div><div class="col">' + obj['intentinput'] + '</div> \
                                            </div>' }
                       
                        
                        //intent
                        if ( obj['intent'] != null && obj['intent'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Intent</div><div class="col">' + obj['intent'] + ' (' + obj['confidenceScore'] + ')</div></div>'
                            if ( obj['slots_id'] !== undefined && obj['slots_id'].length > 0 ) {
                                //slots
                                html += '<div class="row pt-1"><div class="col-2">Slots</div><div class="col">'
                                html += '<table class="table table-sm"><tbody>'
                                html += '<tr><th scope="col pt-1">Slot Name</th><th scope="col">Entity</th><th scope="col">Value</th><th scope="col">Raw Value</th></tr>'
                                for(var z = 0; z < obj['slots_id'].length; z++) {
                                    var slot_obj = obj['slots_id'][z];
                                    html += '<tr><td>' + slot_obj['slotName'] + '</td><td>' + slot_obj['entity'] + '</td><td>' + slot_obj['value'] + '</td><td>' + slot_obj['rawValue'] + '</td></tr>'
                                }
                                html += '</tbody></table></div></div>'
                            }          
                        }
                                    
                        //termination
                        if ( obj['termination'] != null && obj['termination'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2">Termination</div><div class="col">' + obj['terminationreason'] + '</div> \
                                            </div>' }
                        if ( obj['terminationerror'] != null && obj['terminationerror'] !== undefined) {                    
                            html += '<div class="row"><div class="col-2"Termination Error</div><div class="col">' + obj['terminationerror'] + '</div> \
                                            </div>' }
                                            

                        html += '        </div></li>' 
                        
                        $("#timelinelist").append(html);
                    }

                    if (data['rows'].length < 21) {
                        canLoadMore = false;
                        $( "#loadingbox" ).remove();
                        var html = '<li id="compeltedlistbox" class="d-flex justify-content-center timeline-inverted"> \
                            <div class="timeline-body"> \
                                </br>-- End of log --</div></li>' ;
                        $("#timelinelist").append(html);
                    }
                    loadingData = false;
                }
            }
            
        });
    }

    //load the first rows
    load_rows();

    //click event for selecting to filter list by device/site name
    $( "#timelineSites" ).change(function() {
        site = this.value;
        last_date = '2200-01-01'; //reset the date
        canLoadMore = true;
        loadingData = false;
        
        //clear the current page log
        $("#timelinelist").html('');

        //call to load the timeline
        load_rows();
      });

    //scolling
    $(window).scroll(function() {
        //show scroll to top button for not
        if (document.body.scrollTop > 400 || document.documentElement.scrollTop > 400) {
            document.getElementById("myBtn").style.display = "block";
        } else {
            document.getElementById("myBtn").style.display = "none";
        }

        //when scrolling nearly to the bottom.. try to load more rows of data to view
        if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 150)) {
            
            if (loadingData == false && canLoadMore == true) {
                loadingData = true;
                var html = '<li id="loadingbox" class="d-flex justify-content-center timeline-inverted"> \
                                <div class="timeline-body"> \
                                    <div class="spinner-border text-primary" role="status"> \
                                        </br></br><span class="sr-only">Loading more...</span> \
                            </div></div></li>' ;
                $("#timelinelist").append(html);
                
                //call to load the timeline
                load_rows();
            }
        }
    });

    // When the user clicks on the button, scroll to the top of the document
    

}); 

