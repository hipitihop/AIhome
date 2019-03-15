/**
 * File: /Users/gregbail/AIhome2/static/js/Pages/Watch.js
 * Project: Snips Web Admin
 * Created Date: Tuesday, March 12th 2019, 11:44:02 pm
 * Author: Greg
 * -----
 * Last Modified: Wed Mar 13 2019
 * Modified By: Greg
 * -----
 * Copyright (c) 2019 Your Company
 * ------------------------------------
 * Javascript will save your soul!
 */

$(function () {
    "use strict";
    // ============================================================== 
    // get data
    // ============================================================== 

    function load_page(daysbefore) {

        $.getJSON("api/overview/" + daysbefore, function(data) {
            
            var top10 = data.top10;
            var index =0;

            //if (top10.length > 0) {

                var chartmeta = [];
                var chartlabels = [];
                for (index = 0; index < top10.length; ++index) {
                    chartmeta.push({meta: top10[index][1], value: top10[index][0]});
                    chartlabels.push(top10[index][1]);
                }

                var chart = new Chartist.Bar('.amp-pxl', { 
                    labels: chartlabels, 
                    series: [
                        chartmeta
                    ]}
                    , { 
                        axisX: {
                            // On the x-axis start means top and end means bottom
                            position: 'end',
                            showGrid: false
                        },
                        plugins: [
                            Chartist.plugins.tooltip()
                        ]
                    });
                // ============================================================== 
                // This is for the animation
                // ==============================================================
                chart.on('draw', function(data) {
                    data.element.animate({
                        y2: {
                            dur: 500,
                            from: data.y1,
                            to: data.y2,
                            easing: Chartist.Svg.Easing.easeInOutElastic
                        },
                        opacity: {
                            dur: 500,
                            from: 0,
                            to: 1,
                            easing: Chartist.Svg.Easing.easeInOutElastic
                        }
                    });
                });
            //}

            if (top10.length == 0) {
                //nothing in the graph to show
                $("#blankgraph").css("visibility","visible");
            } else {
                $("#blankgraph").css("visibility","hidden");
            }
        
        
            // ============================================================== 
            // sparkline charts
            // ==============================================================
            var sparklines = function() { 

                if (data) {
                    
                    //work out the size of the graph
                    var width = $('#spark8').width() - (5*data.wakeword[1].length); //minus bar spacing * number of bars - for padding
                    width = width / data.wakeword[1].length; //array length


                    $("#wakewordcount").html(data.wakeword[0]);
                    $("#intentsfound").html(data.intentsfound[0]);
                    $("#unknownintents").html(data.unknownintents[0]);
                    $("#errors").html(data.errors[0]);
                    
                    $('#spark8').sparkline(data.wakeword[1], {
                        type: 'bar',
                        width: '100%',
                        height: '70',
                        barWidth: width,
                        resize: true,
                        barSpacing: '5',
                        barColor: '#0F7F12'
                    });
                    $('#spark9').sparkline(data.intentsfound[1], {
                        type: 'bar',
                        width: '100%',
                        height: '70',
                        barWidth: width,
                        resize: true,
                        barSpacing: '5',
                        barColor: '#7460ee'
                    });
                        $('#spark10').sparkline(data.unknownintents[1], {
                        type: 'bar',
                        width: '100%',
                        height: '70',
                        barWidth: width,
                        resize: true,
                        barSpacing: '5',
                        barColor: '#ffb22b'
                    });
                        $('#spark11').sparkline(data.errors[1], {
                        type: 'bar',
                        width: '100%',
                        height: '70',
                        barWidth: width,
                        resize: true,
                        barSpacing: '5',
                        barColor: '#f62d51'
                    });
                }
            }

            var sparkResize;

            $(window).resize(function(e) {
                clearTimeout(sparkResize);
                sparkResize = setTimeout(sparklines, 500);
            });
            
            sparklines();

        });
    }

    load_page(1); //load the default page view for data over 1 day

    //time period in breadcrumb ar click events
    //show either default 24 hrs or 7 days
    $('a[data-toggle="tab"]').on('show.bs.tab', function(e) {
        //get the content href
        var targetpage = $(e.target).attr('href');
        load_page(targetpage);
        //from content href prepare new div id and show content html there
        //$("#new" + contentId.substring(1).capitalizeFirstLetter()).html($("" + contentId).html());
    })
});    
    