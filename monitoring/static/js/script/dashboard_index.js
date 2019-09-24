(function () {
    'use strict';

    var app = angular.module("App", ["ngGrid"])
        .service('DatosService', DatosService)
        .constant('UrlsAcciones', UrlsAcciones)
        .constant('highchartsOpciones', highchartsOpciones)
        .controller('AppCtrl', DatosCtrl);

    DatosCtrl.$inject = ['$scope', 'UrlsAcciones', 'DatosService', 'highchartsOpciones', '$timeout'];

    function DatosCtrl($scope, UrlsAcciones, DatosService, highchartsOpciones, $timeout) {
        $scope.cantidadConsultas = 0;
        $scope.cambioRubrosCantidad = 0;
        $scope.cambioPaisesCantidad = 0;
        $scope.proyecto = null;
        $scope.cargando = true;
        $scope.formulario = {
            paises: [],
            rubros: [],
            mes_fiscal: '10',
            post: true,
            paises_todos: true,
            paises_ninguno: false,
            rubros_todos: true,
            rubros_ninguno: false,
        };
        $scope.paises = [];
        $scope.rubros = [];
        $scope.dataMetas = {};
        $scope.seriesType = {};
        $scope.seriesEdad = {};
        $scope.seriesEducacion = {};
        $scope.seriesFiscal = {};
        $scope.dataTotales = {};
        $scope.dataTotales.total = 0;
        $scope.organizacionesObj = {};
        $scope.organizacionesObj.total = 0;
        $scope.nacionalidad = [];
        $scope.paisEventos = [];
        $scope.eventos = {
            actividades: null,
            eventos: null,
        };
        $scope.cargado = {
            organizaciones: false,
            porSexo: false,
            anioFiscal: false
        };

        $scope.validaCarga = function () {
            $scope.cargando = $scope.cargado.organizaciones && $scope.cargado.porSexo && $scope.cargado.anioFiscal;
            $scope.cargando = !$scope.cargando;
            return $scope.cargando;
        };

        function cargarDatosProyecto(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosProyecto, data)
                .then(function (result) {
                    $scope.proyecto = result.data.proyecto;
                    var urlDefault = 'https://lwr.org/';
                    highchartsOpciones.credits.href = highchartsOpciones.getCreditHref(urlDefault);
                    // if (result.data.proyecto !== null) {
                    //     highchartsOpciones.theme.colors = result.data.proyecto.colores;
                    //     if (result.data.proyecto.url !== null)
                    //         highchartsOpciones.credits.href = highchartsOpciones.getCreditHref(result.data.proyecto.url);
                    // } else {
                        highchartsOpciones.theme.colors = highchartsOpciones.theme.colorsDefault;
                    // }
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosCantidadEventos(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosCantidadEventos, data)
                .then(function (result) {
                    $scope.eventos = result.data.cantidadEventos;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoActividades(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoActividades, data)
                .then(function (result) {
                    var hombres = {name: gettext('Men'), data: []};
                    var mujeres = {name: gettext('Women'), data: []};

                    angular.forEach(result.data.actividades, function (value, key) {
                        hombres.data.push(objetoDataSerie(value, value.m));
                        mujeres.data.push(objetoDataSerie(value, value.f));
                    });


                    $scope.series = [hombres, mujeres];
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosPaises(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosPaises, data)
                .then(function (result) {
                    $scope.paises = result.data.paises;
                    paisesTodosNinguno();
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosRubros(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosRubros, data)
                .then(function (result) {
                    $scope.rubros = result.data.rubros;
                    rubrosTodosNinguno();
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoOrganizaciones(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoOrganizaciones, data)
                .then(function (result) {
                    $scope.organizaciones = result.data.organizaciones.data;
                    $scope.organizacionesObj = result.data.organizaciones;
                    $scope.cargado.organizaciones = true;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosProyectosMetas(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosProyectosMetas, data)
                .then(function (result) {
                    $scope.dataMetas = result.data.proyectos_metas;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoNacionalidad(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoNacionalidad, data)
                .then(function (result) {
                    $scope.nacionalidad = result.data.paisArray;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoPaisEventos(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoPaisEventos, data)
                .then(function (result) {
                    $scope.paisEventos = result.data.paisArray;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoAnioFiscal(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoAnioFiscal, data)
                .then(function (result) {
                    $scope.seriesFiscal = setSeries(result.data.fiscal);
                    $scope.cargado.anioFiscal = true;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoEdad(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoEdad, data)
                .then(function (result) {
                    $scope.seriesEdad = setSeries(result.data.edad);
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoEducacion(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoEducacion, data)
                .then(function (result) {
                    $scope.seriesEducacion = setSeries(result.data.educacion);
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoEventos(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoEventos, data)
                .then(function (result) {
                    var drilldownSeries = [];
                    angular.forEach(result.data.eventos, function (value, key) {
                        drilldownSeries.push(objetoDataSerieDrillDown(value, key));
                    });
                    $scope.drilldownSeries = drilldownSeries;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoTipoParticipante(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoTipoParticipante, data)
                .then(function (result) {
                    $scope.seriesType = setSeries(result.data);
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        function cargarDatosGraficoSexoParticipante(data) {
            DatosService
                .Enviar(UrlsAcciones.UrlDatosGraficoSexoParticipante, data)
                .then(function (result) {
                    $scope.dataTotales = result.data;
                    $scope.cargado.porSexo = true;
                })
                .catch(function (mensaje, codigo) {
                    console.log(codigo + ' => ' + mensaje);
                });
        }

        $scope.limpiarData = function () {
            $scope.cargado = {
                organizaciones: false,
                porSexo: false,
                anioFiscal: false
            };

            $scope.proyecto = null;
            $scope.proyectos = null;
        };

        $scope.cargarDatos = function () {

            $scope.limpiarData();
            var data = angular.copy($scope.formulario);
            if ($scope.cantidadConsultas == 0) data.post = false;
            if ($scope.cambioRubrosCantidad == 0) data.rubros = $scope.getDataRubros();
            if ($scope.cambioPaisesCantidad == 0) data.paises = $scope.getDataPaises();

            $timeout(function () {
                cargarDatosPaises(data);
            }, 1);

            $timeout(function () {
                cargarDatosRubros(data);
            }, 1);

            $timeout(function () {
                cargarDatosProyectosMetas(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoOrganizaciones(data);
            }, 1);

            $timeout(function () {
                cargarDatosCantidadEventos(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoAnioFiscal(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoSexoParticipante(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoEdad(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoEducacion(data);
            }, 1);


            $timeout(function () {
                cargarDatosGraficoPaisEventos(data);
            }, 1);

            $timeout(function () {
                cargarDatosProyecto(data);
            }, 1);


            $timeout(function () {
                cargarDatosGraficoNacionalidad(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoEventos(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoActividades(data);
            }, 1);

            $timeout(function () {
                cargarDatosGraficoTipoParticipante(data);
            }, 1);

            $scope.cantidadConsultas++;

        };

        $scope.refrescar = function () {
            $timeout(function () {
                $scope.cargarDatos();
            }, 10);
        };

        // $scope.$watchCollection('formulario', function () {
        //     $scope.refrescar();
        // });

        $scope.$watchCollection('cargado', function () {
            $scope.validaCarga();
        });

        $scope.$watchCollection('series', function () {
            $timeout(function () {
                var opciones = {
                    chart: {marginTop: 80, zoomType: 'xy', type: 'bar'},
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(UrlsAcciones.nombreGrafico),
                    title: highchartsOpciones.title(UrlsAcciones.nombreGrafico),
                    xAxis: {type: 'category', title: {text: gettext('Activities')},},
                    yAxis: {
                        title: {text: gettext('Amount of people')},
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: gettext('<b>Participants</b><br/>'),
                        pointFormat: '{series.name}: {point.y}<br/>' + gettext('Total:') + '{point.stackTotal}'
                    },
                    legend: {enabled: true},
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                style: {color: 'white'}
                            },
                            stacking: 'normal'
                        }
                    },
                    series: $scope.series,
                    drilldown: {
                        activeDataLabelStyle: {
                            color: 'white',
                            textShadow: '0 0 2px black, 0 0 2px black'
                        },
                        series: $scope.drilldownSeries,
                    }
                };
                $scope.Graficar('participantes', opciones);
            }, 10);
        });

        $scope.$watchCollection('seriesType', function () {
            $timeout(function () {
                var opciones = {
                    chart: {marginTop: 80, zoomType: 'xy', type: 'bar'},
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(UrlsAcciones.nombreGrafico),
                    title: highchartsOpciones.title(gettext("PARTICIPANTS BY TYPE OF PERSON")),
                    xAxis: {
                        categories: $scope.seriesType.categorias,
                        title: {text: gettext('Types')},
                    },
                    yAxis: {
                        title: {text: gettext('Amount of people')},
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: gettext('<b>Participants</b><br/>'),
                        pointFormat: '{series.name}: {point.y}<br/>' + gettext('Total:') + '{point.stackTotal}'
                    },
                    legend: {enabled: true},
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                style: {color: 'white'}
                            },
                            stacking: 'normal'
                        }
                    },
                    series: $scope.seriesType.series,

                };
                $scope.Graficar('participantes-tipo', opciones);
            }, 10);
        });

        $scope.$watchCollection('seriesEdad', function () {
            $timeout(function () {
                var opciones = {
                    chart: {marginTop: 80, zoomType: 'xy', type: 'column'},
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(UrlsAcciones.nombreGrafico),
                    title: highchartsOpciones.title(gettext("PARTICIPANTS BY AGE")),
                    xAxis: {
                        categories: $scope.seriesEdad.categorias,
                        title: {text: gettext('Ages')},
                    },
                    yAxis: {
                        title: {text: 'Amount of people'},
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<b>Participants</b><br/>',
                        pointFormat: '{series.name}: {point.y}<br/>' + gettext('Total:') + '{point.stackTotal}'
                    },
                    legend: {enabled: true},
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                style: {color: 'white'}
                            },
                            stacking: 'normal'
                        }
                    },
                    series: $scope.seriesEdad.series,

                };
                $scope.Graficar('participantes-edad', opciones);
            }, 10);
        });

        $scope.$watchCollection('seriesFiscal', function () {
            $timeout(function () {
                var opciones = {
                    chart: {marginTop: 80, zoomType: 'xy', type: 'column'},
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(UrlsAcciones.nombreGrafico),
                    title: highchartsOpciones.title(gettext("PARTICIPANTS BY FISCAL YEAR")),
                    xAxis: {
                        categories: $scope.seriesFiscal.categorias,
                        title: {text: gettext('Years')},
                    },
                    yAxis: {
                        title: {
                            text: gettext('Amount of people')
                        },
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: gettext('<b>Participants</b><br/>'),
                        pointFormat: '{series.name}: {point.y}<br/>' + gettext('Total:') + '{point.stackTotal}'
                    },
                    legend: {enabled: true},
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                style: {color: 'white'}
                            },
                            stacking: 'normal'
                        }
                    },
                    series: $scope.seriesFiscal.series,

                };
                $scope.Graficar('participantes-fiscal', opciones);
            }, 10);
        });

        $scope.$watchCollection('seriesEducacion', function () {
            $timeout(function () {
                var opciones = {
                    chart: {marginTop: 80, zoomType: 'xy', type: 'bar'},
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(UrlsAcciones.nombreGrafico),
                    title: highchartsOpciones.title(gettext("PARTICIPANTS BY EDUCATION")),
                    xAxis: {
                        categories: $scope.seriesEducacion.categorias,
                        title: {text: gettext('Education')},
                    },
                    yAxis: {
                        title: {text: gettext('Amount of people')},
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: gettext('<b>Participants</b><br/>'),
                        pointFormat: '{series.name}: {point.y}<br/>' + gettext('Total:') + '{point.stackTotal}'
                    },
                    legend: {enabled: true},
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                style: {color: 'white'}
                            },
                            stacking: 'normal'
                        }
                    },
                    series: $scope.seriesEducacion.series,

                };
                $scope.Graficar('participantes-educacion', opciones);
            }, 10);
        });

        // $scope.$watchCollection('nacionalidad', function () {
        //     $timeout(function () {
        //         $scope.mapaPaises($scope.nacionalidad, 'participantes-nacionalidad', gettext('Participants by Nationality'));
        //     }, 10);
        // });

        $scope.$watchCollection('paisEventos', function () {
            $timeout(function () {
                $scope.mapaPaises($scope.paisEventos, 'pais-eventos', gettext('Geographic location of participants'));
            }, 10);
        });

        $scope.mapaPaises = function (paises, divMapa, tituloMapa) {
            // New map-pie series type that also allows lat/lon as center option.
            // Also adds a sizeFormatter option to the series, to allow dynamic sizing
            // of the pies.
            Highcharts.seriesType('mappie', 'pie', {
                center: null, // Can't be array by default anymore
                clip: true, // For map navigation
                states: {hover: {halo: {size: 5}}},
                dataLabels: {enabled: false}
            }, {
                getCenter: function () {
                    var options = this.options,
                        chart = this.chart,
                        slicingRoom = 2 * (options.slicedOffset || 0);
                    if (!options.center) {
                        options.center = [null, null]; // Do the default here instead
                    }
                    // Handle lat/lon support
                    if (options.center.lat !== undefined) {
                        var point = chart.fromLatLonToPoint(options.center);
                        options.center = [
                            chart.xAxis[0].toPixels(point.x, true),
                            chart.yAxis[0].toPixels(point.y, true)
                        ];
                    }
                    // Handle dynamic size
                    if (options.sizeFormatter) {
                        options.size = options.sizeFormatter.call(this);
                    }
                    // Call parent function
                    var result = Highcharts.seriesTypes.pie.prototype.getCenter.call(this);
                    // Must correct for slicing room to get exact pixel pos
                    result[0] -= slicingRoom;
                    result[1] -= slicingRoom;
                    return result;
                },
                translate: function (p) {
                    this.options.center = this.userOptions.center;
                    this.center = this.getCenter();
                    return Highcharts.seriesTypes.pie.prototype.translate.call(this, p);
                }
            });

            var data = [];
            //País en ingles, total, mujeres, hombres, coordenada x, cooredenada y, pais en español, alfa2
            Highcharts.each(paises, function (row) {
                data.push(row);
            });

            var maxTotal = 0,
                mujeresColor = 'rgba(74,131,240,0.80)',
                hombresColor = 'rgba(220,71,71,0.80)';


            // Compute max votes to find relative sizes of bubbles
            Highcharts.each(data, function (row) {
                maxTotal = Math.max(maxTotal, row[1]);
            });
            // Build the chart
            var chart = Highcharts.mapChart(divMapa, {
                title: highchartsOpciones.title(tituloMapa),

                mapNavigation: {enabled: true},
                // Limit zoom range
                yAxis: {
                    // minRange: 2300
                },
                credits: highchartsOpciones.credits,
                tooltip: {useHTML: true},

                // Default options for the pies
                plotOptions: {
                    mappie: {
                        borderColor: 'rgba(255,255,255,0.4)',
                        borderWidth: 1,
                        tooltip: {headerFormat: ''}
                    }
                },
                legend: {enabled: false},

                series: [{
                    mapData: Highcharts.maps['custom/world'],
                    nullColor: '#00AAA7',
                    data: data,
                    name: gettext('Participants by Nationality'),
                    borderColor: '#FFF',
                    showInLegend: false,
                    joinBy: ['name', 'id'],
                    keys: [
                        'id', 'total', 'mujeres', 'hombres',
                        'lat', 'lon', 'pais', 'country'
                    ],
                    tooltip: {
                        headerFormat: '',
                        pointFormatter: function () {
                            var hoverVotes = this.hoverVotes; // Used by pie only
                            var tooltip = gettext('<b>Participants ') + this.pais + '</b><br/>' +
                                Highcharts.map([
                                    [gettext('Men'), this.hombres, hombresColor],
                                    [gettext('Women'), this.mujeres, mujeresColor]
                                ].sort(function (a, b) {
                                    return b[1] - a[1]; // Sort tooltip by most votes
                                }), function (line) {
                                    return '<span style="color:' + line[2] +
                                        // Colorized bullet
                                        '">\u25CF</span> ' +
                                        // Party and votes
                                        (line[0] === hoverVotes ? '<b>' : '') +
                                        line[0] + ': ' +
                                        Highcharts.numberFormat(line[1], 0) +
                                        (line[0] === hoverVotes ? '</b>' : '') +
                                        '<br>';
                                }).join('') +
                                gettext('<br/><b>Total Participants: </b>') + Highcharts.numberFormat(this.total, 0);

                            if (this.eventos !== undefined) {
                                tooltip = tooltip + gettext('<br/><b>Events: </b>') + Highcharts.numberFormat(this.eventos, 0);
                            }
                            return tooltip;
                        }
                    }
                },
                    {
                        name: 'Connectors',
                        type: 'mapline',
                        color: 'rgba(130, 130, 130, 0.5)',
                        zIndex: 5,
                        showInLegend: false,
                        enableMouseTracking: false
                    }
                ]
            });


            // Add the pies after chart load, optionally with offset and connectors
            Highcharts.each(chart.series[0].points, function (state) {
                if (!state.id) {
                    return; // Skip points with no data, if any
                }
                var pieOffset = state.pieOffset || {},
                    centerLat = parseFloat(state.lat),
                    centerLon = parseFloat(state.lon);

                // Add the pie for this state
                chart.addSeries({
                    type: 'mappie',
                    zIndex: 6, // Keep pies above connector lines
                    sizeFormatter: function () {
                        var yAxis = this.chart.yAxis[0],
                            zoomFactor = (yAxis.dataMax - yAxis.dataMin) /
                                (yAxis.max - yAxis.min);
                        return Math.max(
                            this.chart.chartWidth / 250 * zoomFactor, // Min size
                            this.chart.chartWidth / 200 * zoomFactor * state.total / maxTotal
                        );
                    },
                    tooltip: {
                        // Use the state tooltip for the pies as well
                        pointFormatter: function () {
                            return state.series.tooltipOptions.pointFormatter.call({
                                id: state.id,
                                hoverVotes: this.name,
                                pais: state.pais,
                                mujeres: state.mujeres,
                                hombres: state.hombres,
                                total: state.total,
                                eventos: state.eventos
                            });
                        }
                    },

                    data: [{
                        name: gettext('Men'),
                        y: state.hombres,
                        color: hombresColor
                    }, {
                        name: gettext('Women'),
                        y: state.mujeres,
                        color: mujeresColor
                    }],
                    center: {
                        lat: centerLat + (pieOffset.lat || 0),
                        lon: centerLon + (pieOffset.lon || 0)
                    }
                }, false);

                // Draw connector to state center if the pie has been offset
                if (pieOffset.drawConnector !== false) {
                    var centerPoint = chart.fromLatLonToPoint({
                            lat: centerLat,
                            lon: centerLon
                        }),
                        offsetPoint = chart.fromLatLonToPoint({
                            lat: centerLat + (pieOffset.lat || 0),
                            lon: centerLon + (pieOffset.lon || 0)
                        });
                    chart.series[2].addPoint({
                        name: state.id,
                        path: 'M' + offsetPoint.x + ' ' + offsetPoint.y +
                            'L' + centerPoint.x + ' ' + centerPoint.y
                    }, false);
                }
            });
            // Only redraw once all pies and connectors have been added
            chart.redraw();
        };

        $scope.$watchCollection('dataTotales', function () {
            $timeout(function () {
                var opciones = {
                    chart: {
                        marginTop: 80,
                        zoomType: 'xy',
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                        type: 'pie'
                    },
                    title: highchartsOpciones.title(gettext('Participants reached, by sex')),
                    subtitle: {text: gettext('Total amount') + ' ' + $scope.dataTotales.total},
                    tooltip: {pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'},
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} % , {point.y}',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    legend: {enabled: true},
                    series: [{
                        name: gettext('Participants'),
                        colorByPoint: true,
                        data: [{
                            name: gettext('Men'),
                            y: parseFloat($scope.dataTotales.m)
                        }, {
                            name: gettext('Women'),
                            y: parseFloat($scope.dataTotales.f),
                            sliced: true,
                        }]
                    }],

                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(gettext('Participants')),
                };
                $scope.Graficar('pastel', opciones);
            }, 10);
        });

        $scope.$watchCollection('organizaciones', function () {
            $timeout(function () {
                var opciones = {

                    title: highchartsOpciones.title(gettext('ORGANIZATIONS')),
                    subtitle: {text: $scope.organizacionesObj.total + ' ' + gettext('total, in') + ' ' + $scope.organizacionesObj.total_categorias + ' ' + gettext('Categories')},

                    series: [{
                        type: 'treemap',
                        layoutAlgorithm: 'squarified',
                        allowDrillToNode: true,
                        animationLimit: 1000,
                        dataLabels: {
                            enabled: false
                        },
                        levelIsConstant: false,
                        levels: [{
                            level: 1,
                            dataLabels: {
                                enabled: true
                            },
                            borderWidth: 3
                        }],
                        data: $scope.organizacionesObj.data
                    }],
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(gettext('Organizations')),
                };
                $scope.Graficar('organizaciones', opciones);
            }, 10);
        });

        $scope.$watchCollection('dataMetas', function () {
            $timeout(function () {
                var opciones = {
                    chart: {
                        type: 'bar',
                        marginTop: 80,
                        zoomType: 'xy',
                        plotBackgroundColor: null,
                        plotBorderWidth: null,
                        plotShadow: false,
                    },
                    // title: highchartsOpciones.title('METAS POR PROYECTO'),
                    title: highchartsOpciones.title(gettext('Total participants achieved and goals, by sex')),
                    // subtitle: {text: $scope.organizacionesObj.total + ' total, en ' + $scope.organizacionesObj.total_categorias + ' Categorías'},

                    xAxis: {categories: $scope.dataMetas.categorias},

                    yAxis: [{
                        min: 0,
                        title: {text: gettext('Persons')}
                    }],
                    legend: {shadow: false},
                    tooltip: {shared: true},
                    plotOptions: {
                        bar: {
                            grouping: false,
                            shadow: false,
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                // format: '<b>{point.name}</b>: {point.percentage:.1f} % , {point.y}',
                                style: {
                                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                                }
                            }
                        }
                    },
                    series: $scope.dataMetas.series,
                    credits: highchartsOpciones.credits,
                    exporting: highchartsOpciones.exporting(gettext('Goals')),
                };
                $scope.Graficar('metas', opciones);
            }, 10);
        });

        $scope.Graficar = function (div, opcions) {
            Highcharts.theme = highchartsOpciones.theme;
            Highcharts.setOptions(Highcharts.theme);

            Highcharts.chart(div, opcions, function (chart) { // on complete
                // chart.renderer.image(UrlsAcciones.UrlLogo, 20, 5, 100, 50).add();
            });
        };

        $scope.estado = function (estado) {
            if (estado === '1')
                return '0';
            else
                return '1';
        };

        $scope.getDataPaises = function () {
            var result = [];
            var array = angular.copy($scope.paises);
            angular.forEach(array, function (value, key) {
                if (value.active) {
                    var id = value.id == 0 ? null : value.id;
                    result.push(id);
                }
            });
            return result;
        };

        $scope.cambioPaises = function () {
            $scope.cambioPaisesCantidad++;
            $scope.formulario.paises = $scope.getDataPaises();
        };

        $scope.getDataRubros = function () {
            var result = [];
            var array = angular.copy($scope.rubros);
            angular.forEach(array, function (value, key) {
                if (value.active) {
                    var id = value.id == 0 ? null : value.id;
                    result.push(id);
                }
            });
            return result;
        };

        $scope.cambioRubros = function () {
            $scope.cambioRubrosCantidad++;
            $scope.formulario.rubros = $scope.getDataRubros();
        };

        $scope.classChecked = function (obj) {
            return $scope.isChecked(obj) ? 'active' : '';
        };

        $scope.iconChecked = function (obj) {
            return $scope.isChecked(obj) ? 'fa-check' : '';
        };

        $scope.isChecked = function (obj) {
            return obj.active ? true : false;
        };


        $scope.PaisesTodos = function () {
            $scope.formulario.paises_todos = true;
            $scope.formulario.paises_ninguno = false;
            $scope.seleccionarPaises();
        };

        $scope.RubrosTodos = function () {
            $scope.formulario.rubros_todos = true;
            $scope.formulario.rubros_ninguno = false;
            $scope.seleccionarRubros();
        };

        $scope.PaisesNinguno = function () {
            $scope.formulario.paises_ninguno = true;
            $scope.formulario.paises_todos = false;
            $scope.seleccionarPaises();
        };

        $scope.RubrosNinguno = function () {
            $scope.formulario.rubros_ninguno = true;
            $scope.formulario.rubros_todos = false;
            $scope.seleccionarRubros();
        };

        function verificaValorArray(array, val) {
            var valor = true;
            angular.forEach(array, function (value, key) {
                valor &= value.active == val;
            });
            return valor;
        }

        function rubrosTodosNinguno() {
            $scope.formulario.rubros_todos = verificaValorArray($scope.rubros, true);
            $scope.formulario.rubros_ninguno = verificaValorArray($scope.rubros, false);
        }

        function paisesTodosNinguno() {
            $scope.formulario.paises_todos = verificaValorArray($scope.paises, true);
            $scope.formulario.paises_ninguno = verificaValorArray($scope.paises, false);
        }

        $scope.selectedPaisClick = function (obj) {
            obj.active = !obj.active;
            paisesTodosNinguno();
            $scope.seleccionarPaises();
        };

        $scope.selectedRubroClick = function (obj) {
            obj.active = !obj.active;
            rubrosTodosNinguno();
            $scope.seleccionarRubros();
        };

        function cambiarEstadoArray(array, val) {
            angular.forEach(array, function (value, key) {
                value.active = val;
            });
        }

        $scope.seleccionarPaises = function () {
            if ($scope.formulario.paises_todos)
                cambiarEstadoArray($scope.paises, true);

            if ($scope.formulario.paises_ninguno)
                cambiarEstadoArray($scope.paises, false);
            $scope.cambioPaises();
        };

        $scope.seleccionarRubros = function () {
            if ($scope.formulario.rubros_todos)
                cambiarEstadoArray($scope.rubros, true);

            if ($scope.formulario.rubros_ninguno)
                cambiarEstadoArray($scope.rubros, false);
            $scope.cambioRubros();
        };

        function objetoDataSerie(value, valorY) {
            var obj = {};
            var name = !value.name ? 'NE' : value.name;
            obj.name = name;
            obj.drilldown = 'Event_' + value.activity_id;
            obj.y = parseFloat(valorY);
            return obj;
        }

        function setSeries(data) {
            var type = {};
            type.categorias = [];
            type.series = [];
            var typeHombres = {};
            typeHombres.name = gettext('Men');
            typeHombres.data = [];
            var typeMujeres = {};
            typeMujeres.name = gettext('Women');
            typeMujeres.data = [];
            angular.forEach(data, function (value, key) {
                type.categorias.push(value.type);
                typeHombres.data.push(parseFloat(value.m));
                typeMujeres.data.push(parseFloat(value.f));
            });
            type.series.push(typeHombres);
            type.series.push(typeMujeres);
            return type;
        }

        function objetoDataSerieDrillDown(value, key) {
            var obj = {};
            obj.id = null;
            obj.name = null;
            obj.data = [];
            angular.forEach(value, function (evento, key) {
                if (!obj.id)
                    obj.id = 'Event_' + evento.activity_id;
                if (!obj.name)
                    obj.name = !evento.activity ? 'NE' : evento.activity;

                obj.data.push([evento.name, parseFloat(evento.total)]);
            });
            return obj;
        }

        $scope.refrescar();
    }

})();