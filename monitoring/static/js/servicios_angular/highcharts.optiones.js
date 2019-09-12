highchartsOpciones = {
    theme: {
        lang: {
            drillUpText: '◁ '+gettext('Return'),
            months: [gettext('January'), gettext('February'), gettext('March'), gettext('April'), gettext('May'), gettext('June'), gettext('July'), gettext('August'), gettext('September'), gettext('October'), gettext('November'), gettext('December')],
            shortMonths: [gettext('Jan'), gettext('Feb'), gettext('Mar'), gettext('Apr'), gettext('May'), gettext('Jun'), gettext('Jul'), gettext('Aug'), gettext('Sept'), gettext('Oct'), gettext('Nov'), gettext('Dec')],
            downloadPDF: gettext('File PDF'),
            downloadJPEG: gettext('Image JPEG'),
            downloadPNG: gettext('Image PNG'),
            downloadSVG: gettext('Image SVG'),
            printChart: gettext('Print Chart'),
            resetZoom: gettext('Reset Zoom'),
            resetZoomTitle: gettext('Reset Zoom'),
            downloadCSV: gettext("Download CSV"),
            downloadXLS: gettext("Download Excel XLS"),
            openInCloud: gettext("Open in Highcharts Cloud"),
            viewData: gettext("Display data table")
        },
        colors: ['#B2BB1E', '#00AAA7', '#472A2B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        colorsDefault: ['#B2BB1E', '#00AAA7', '#472A2B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
//        colors: [ '#B2BB1E', '#472A2B','#00AAA7', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],

        chart: {
            backgroundColor: {
                linearGradient: {x1: 0, y1: 0, x2: 1, y2: 1},
                stops: [
                    [0, 'rgb(255, 255, 255)'],
                    [1, 'rgb(240, 240, 255)']
                ]
            },
            borderWidth: 0,
            plotBackgroundColor: 'rgba(255, 255, 255, .9)',
            plotShadow: true,
            plotBorderWidth: 1
        },
        title: {
            style: {
                color: '#000',
                font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
            }
        },
        subtitle: {
            style: {
                color: '#666666',
                font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
            }
        },
        xAxis: {
            gridLineWidth: 1,
            lineColor: '#000',
            tickColor: '#000',
            labels: {
                style: {
                    color: '#000',
                    font: '11px Trebuchet MS, Verdana, sans-serif'
                }
            },
            title: {
                style: {
                    color: '#333',
                    fontWeight: 'bold',
                    fontSize: '12px',
                    fontFamily: 'Trebuchet MS, Verdana, sans-serif'

                }
            }
        },
        yAxis: {
            minorTickInterval: 'auto',
            lineColor: '#000',
            lineWidth: 1,
            tickWidth: 1,
            tickColor: '#000',
            labels: {
                style: {
                    color: '#000',
                    font: '11px Trebuchet MS, Verdana, sans-serif'
                }
            },
            title: {
                style: {
                    color: '#333',
                    fontWeight: 'bold',
                    fontSize: '12px',
                    fontFamily: 'Trebuchet MS, Verdana, sans-serif'
                }
            }
        },
        legend: {
            itemStyle: {
                font: '9pt Trebuchet MS, Verdana, sans-serif',
                color: 'black'

            },
            itemHoverStyle: {color: '#039'},
            itemHiddenStyle: {color: 'gray'}
        },
        labels: {style: {color: '#99b'}},

        navigation: {buttonOptions: {theme: {stroke: '#CCCCCC'}}}
    },
    lang: {
        months: [gettext('January'), gettext('February'), gettext('March'), gettext('April'), gettext('May'), gettext('June'), gettext('July'), gettext('August'), gettext('September'), gettext('October'), gettext('November'), gettext('December')],
        shortMonths: [gettext('Jan'), gettext('Feb'), gettext('Mar'), gettext('Apr'), gettext('May'), gettext('Jun'), gettext('Jul'), gettext('Aug'), gettext('Sept'), gettext('Oct'), gettext('Nov'), gettext('Dec')],
        downloadPDF: gettext('File PDF'),
        downloadJPEG: gettext('Image JPEG'),
        downloadPNG: gettext('Image PNG'),
        downloadSVG: gettext('Image SVG'),
        printChart: gettext('Print Chart'),
        resetZoom: gettext('Reset Zoom'),
        resetZoomTitle: gettext('Reset Zoom'),
    },

    credits: {
        enabled: true,
        href: getCreditHref('#'),
        text: gettext('All rights reserved LWR')
    },
    exporting: function (val) {
        return {sourceWidth: 1200, sourceHeight: 400, filename: val};
    },
    title: function (val) {
        return{text: val, style: {color: '#B2BB1E', fontWeight: 'bold', }};
    },
    getCreditHref: function (url) {
        return 'javascript:window.open("' + url + '", "_blank")';
    }
};

function getCreditHref(url) {
    return 'javascript:window.open("' + url + '", "_blank")';
}
