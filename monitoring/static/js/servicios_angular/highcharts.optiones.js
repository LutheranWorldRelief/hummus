highchartsOpciones = {
    theme: {
        lang: {
            drillUpText: '◁ Regresar',
            months: ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
            shortMonths: ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'],
            downloadPDF: 'Archivo PDF',
            downloadJPEG: 'Imagén JPEG',
            downloadPNG: 'Imagén PNG',
            downloadSVG: 'Imagén SVG',
            printChart: 'Imprimir Gráfico',
            resetZoom: 'Reestablecer Zoom',
            resetZoomTitle: 'Reestablecer Zoom',
            downloadCSV: "Descargar CSV",
            downloadXLS: "Descargar Excel XLS",
            openInCloud: "Abrir en Highcharts Cloud",
            viewData: "Visualizar tabla de datos"
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
        months: ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
        shortMonths: ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'],
        downloadPDF: 'Archivo PDF',
        downloadJPEG: 'Imagén JPEG',
        downloadPNG: 'Imagén PNG',
        downloadSVG: 'Imagén SVG',
        printChart: 'Imprimir Gráfico',
        resetZoom: 'Reestablecer Zoom',
        resetZoomTitle: 'Reestablecer Zoom',
    },

    credits: {
        enabled: true,
        href: getCreditHref('#'),
        text: 'Todos los derechos reservados LWR'
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
