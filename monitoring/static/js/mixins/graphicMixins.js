var graphicMixins = {
    data() {
        return {
            typeGraphic: null,
            background_color: '#fff',
            colors: {
                men: array_colors_lwr[1],
                women: array_colors_lwr[0]
            },
            names_legends: [
                gettext('Men'),
                gettext('Women')
            ],
            icon_graph: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
        }
    },
    methods: {
        graphicParticipants(type) {
            return new Promise((resolved, reject) => {
                let myChart = echarts.init(document.getElementById(type === 'GraphicQuarter' ? 'TrimestralGraph' : 'FiscalYearGraph'));

                let series = [
                    {
                        name: 'Men',
                        type: 'bar',
                        stack: true,
                        label: {
                            normal: {
                                show: true,
                                position: 'insideRight'
                            }
                        },
                        data: type === 'GraphicQuarter' ? this.hombresQ : this.hombres
                    },
                    {
                        name: 'Women',
                        type: 'bar',
                        stack: true,
                        label: {
                            normal: {
                                show: true,
                                position: 'insideRight'
                            }
                        },
                        data: type === 'GraphicQuarter' ? this.mujeresQ : this.mujeres
                    },
                    {
                        name: 'null',
                        data: type === 'GraphicQuarter' ? this.defauldSerieQ : this.defauldSerie
                    }
                ];

                function isLastSeries(index) {
                    return index === series.length - 1
                }

                let text_label = type === 'GraphicQuarter' ? 'Participants by quarter' : 'Participants by fiscal year';
                let option = {
                    toolbox: this.setToolBox(text_label),
                    color: [this.colors.men, this.colors.women],
                    backgroundColor: this.background_color,
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow' //'line' | 'shadow'
                        }, formatter: function (params) {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                if (item.seriesName != 'null')
                                    axisValue += `<p>${item.marker} ${item.seriesName}: ${item.data}</p>`;
                            });
                            return axisValue;
                        },
                    },
                    legend: {
                        data: this.names_legends,
                        center: 'right'
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '6%',
                        containLabel: true
                    },
                    "calculable": true,
                    xAxis: [{
                        type: 'category',
                        position: 'bottom',
                        data: type === 'GraphicQuarter' ? this.aniosQ : this.anios,
                        axisLabel: {
                            rotate: 90,
                            verticalAlign: 'middle',
                        },
                    }],
                    yAxis: {
                        type: 'value'
                    }, //Sumar valores de la serie (cantidad hombres y mujeres por año)
                    series: series.map((item, index) => Object.assign(item, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series) : null,
                            fontSize: isLastSeries(index) ? 13 : 11,
                            color: isLastSeries(index) ? '#4f5f6f' : '#000',
                            position: isLastSeries(index) ? 'top' : 'inside',
                            verticalAlign: 'middle',
                            distance: 30,
                        },
                    }))
                };

                if (type === 'GraphicQuarter') {
                    //Barra para realizar Zoom
                    option.dataZoom = [{
                        "show": true,
                        "height": 20,
                        "xAxisIndex": [
                            0
                        ],
                        bottom: 0,
                        "start": 50,
                        "end": 100,
                        handleIcon: this.icon_graph,
                        handleSize: '110%',
                        handleStyle: {
                            color: 'rgba(144,151,156,.8)',
                        },
                        textStyle: {
                            color: "#000"
                        },
                        borderColor: "#90979c"
                    }, {
                        "type": "inside",
                        "show": true,
                        "height": 15,
                        "start": 1,
                        "end": 35
                    }]
                }

                myChart.setOption(option);

                myChart.on('legendselectchanged', (params) => {
                    let gender = '';
                    let selected = params.selected;
                    if (selected.Men && selected.Women) {
                        gender = null;
                    } else if (!selected.Men && selected.Women) {
                        gender = this.names_legends[1];
                    } else if (selected.Men && !selected.Women) {
                        gender = this.names_legends[0];
                    }

                    option.series.map((item, index) => Object.assign(item, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series, gender) : null,
                            fontSize: isLastSeries(index) ? 13 : 11,
                            color: isLastSeries(index) ? '#4f5f6f' : '#000',
                            position: isLastSeries(index) ? 'top' : 'inside',
                            rotate: 90,
                            verticalAlign: 'middle',
                            distance: 30,
                        },
                    }));

                    myChart.setOption(option);
                });
                this.responsiveChart('#tab_quarter-click li', myChart);

                resolved(true);
            });
        },
        graficoMetas() {

            let myChart = echarts.init(document.getElementById('MetaParticipantes'));

            // TODO Inicio Asignar meta
            var meta = [];
            this.totalByBar.forEach(function (numero, index) {
                if (Math.floor(Math.random() * 10) % 2 === 0)
                    meta.push(numero + (index * 100));
                else if (numero < 200)
                    meta.push(numero + (300));
                else
                    meta.push(numero - (1000));
            });
            this.metaPoranio = meta;
            /**
             *
             * Fin
             */
            var label = {
                normal: {
                    show: true,
                    position: 'top',
                    distance: 15,
                    verticalAlign: 'middle',
                    formatter: function (param) {
                        return param.value;
                    },
                    textStyle: {
                        color: 'rgba(0,0,0,.7)',
                        fontSize: '11',
                        fontWeight: '560',
                    }
                }
            };

            var option = {
                toolbox: this.setToolBox('Assigned Goal - Amound Goal'),
                backgroundColor: this.background_color,
                grid: {
                    left: '3%',
                    right: '3%',
                    bottom: '10%',
                    top: '10%',
                    containLabel: true
                },
                tooltip: {
                    show: "true",
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow',// 'line' | 'shadow'
                        shadowStyle: {
                            color: 'rgba(112,112,112,0)',
                        },
                    },
                    formatter: function (params) {
                        let axisValue = `<p>${params[0].axisValue}</p>`;
                        params.forEach(item => {
                            axisValue += `<p>${item.marker} ${item.seriesName}: ${item.data}</p>`;
                        });
                        return axisValue;
                    },
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    padding: [6, 6],
                    extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);',
                },
                legend: {
                    bottom: 'bottom',
                    textStyle: {
                        color: '#4f5f6f',
                    },
                    data: [gettext('Actual'), gettext('Meta')],
                },
                xAxis: [{
                    type: 'category',
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: '#363e83',
                        }
                    },
                    axisLabel: {//Eje x
                        rotate: 90,
                        verticalAlign: 'middle',
                        textStyle: {
                            color: '#4f5f6f',
                            fontWeight: '500',
                            fontSize: '12',
                        },
                    },
                    data: this.anios //xAxisData
                }, {
                    type: 'category',
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: 'rgba(50,52,108,.1)',
                        }
                    },
                    axisLabel: {//Barra horizontal arriba
                        verticalAlign: 'middle',
                        textStyle: {
                            color: 'rgba(0,0,0,.6)',
                            fontSize: '11',
                            fontWeight: '560',
                        },
                        margin: 20,
                    },
                    data: this.metaPoranio
                }, {
                    type: 'category',
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        show: false
                    },
                    splitArea: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },//Anios en el tooltip
                    data: this.anios
                }],
                yAxis: {
                    type: 'value',
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: '#32346c',
                        }
                    },
                    splitLine: { //Lineas horizontales en el plano
                        show: true,
                        lineStyle: {
                            color: 'rgba(50,52,108,.1)',
                        }
                    },
                    axisLabel: {
                        textStyle: {
                            color: '#4f5f6f',
                            fontWeight: 'normal',
                            fontSize: '11',
                        },
                    },
                },
                series: [{
                    name: gettext('Actual'),
                    type: 'bar',
                    stack: '1',
                    xAxisIndex: 0,
                    data: this.totalByBar,
                    label: label,
                    barGap: '-100%',
                    barWidth: '35%',
                    itemStyle: {
                        normal: {
                            color: array_colors_lwr[1],
                        }
                    },
                    z: 2
                }, {
                    name: gettext('Meta'),
                    type: 'bar',
                    xAxisIndex: 2,
                    data: this.metaPoranio,
                    barWidth: '67%',
                    itemStyle: {
                        normal: {
                            color: 'rgba(4,170,171,0.6)',
                            barBorderRadius: 1,
                        }
                    },
                    z: 1
                }]
            };
            this.responsiveChart('#tab_quarter-click', myChart);
            myChart.setOption(option);
        },
        graficoMetasLinea() {

            let myChart = echarts.init(document.getElementById('MetaParticipantesPorSexo'));

            option = {
                toolbox: this.setToolBox('Assigned Goal - Amound Goal by Sex'),
                backgroundColor: this.background_color,
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {
                        "type": "shadow",
                        textStyle: {
                            color: "#fff"
                        }
                    },
                },
                "grid": {
                    "borderWidth": 0,
                    "top": 110,
                    "bottom": 95,
                    textStyle: {
                        color: "#fff"
                    }
                },
                "legend": {
                    x: '40%',
                    top: '7%',
                    align: 'right',
                    textStyle: {
                        color: '#90979c',
                    },
                    "data": [gettext('Men'), gettext('Woman'), gettext('Meta')]
                },
                "calculable": true,
                "xAxis": [{
                    "type": "category",
                    "axisLine": {
                        lineStyle: {
                            color: '#90979c'
                        }
                    },
                    "splitLine": {
                        "show": false
                    },
                    "axisTick": {
                        "show": false
                    },
                    "splitArea": {
                        "show": false
                    },
                    "axisLabel": {
                        "interval": 0,
                        rotate: 90,
                        verticalAlign: 'middle',
                        textStyle: {
                            color: '#4f5f6f',
                            fontWeight: '500',
                            fontSize: '12',
                        },
                    },
                    "data": this.anios,
                }],
                "yAxis": [{
                    "type": "value",
                    "splitLine": {
                        "show": false
                    },
                    "axisLine": {
                        lineStyle: {
                            color: '#90979c'
                        }
                    },
                    "axisTick": {
                        "show": false
                    },
                    "axisLabel": {
                        "interval": 0,
                    },
                    "splitArea": {
                        "show": false
                    },
                }],
                "dataZoom": this.getGraphicZoom(),
                "series": [{
                    "name": gettext("Men"),
                    "type": "bar",
                    "barMaxWidth": 35,
                    "barGap": "20%",
                    "itemStyle": {
                        "normal": {
                            "color": array_colors_lwr[1],
                            "label": {
                                "show": true,
                                "position": "inside",
                                color: 'rgba(0,0,0,0.6)',
                                fontWeight: '550',
                                fontSize: '11', //insideTop
                                formatter: function (p) {
                                    return p.value > 0 ? (p.value) : '';
                                }
                            }
                        }
                    },
                    "data": this.hombres
                }, {
                    "name": gettext("Woman"),
                    "type": "bar",
                    "itemStyle": {
                        "normal": {
                            "color": array_colors_lwr[0],
                            "barBorderRadius": 0,
                            "label": {
                                "show": true,
                                "position": "inside",
                                color: 'rgba(0,0,0,0.6)',
                                fontWeight: '550',
                                fontSize: '11',
                                formatter: function (p) {
                                    return p.value > 0 ? (p.value) : '';
                                }
                            }
                        }
                    },
                    "data": this.mujeres
                }, {
                    "name": gettext('Meta'),
                    "type": "line",
                    "stack": true,
                    symbolSize: 10,
                    position: 'fixed',
                    symbol: 'circle',
                    "itemStyle": {
                        "normal": {
                            "color": 'rgba(49,147,218,0.5)',
                            "barBorderRadius": 0,
                            "label": {
                                "show": true,
                                "position": "top",
                                fontWeight: '570',
                                fontSize: '12',
                                distance: 35,
                                formatter: function (p) {
                                    return p.value > 0 ? (p.value) : '';
                                }
                            }
                        }
                    },
                    "data": this.metaPoranio
                },
                ]
            };
            this.responsiveChart('', myChart);
            myChart.setOption(option);
        },
        graficoParticipantesEdad() {
            $.post(UrlsAcciones.UrlGraficoEdad, this.requestParameters)
                .then(response => {
                    let data = response.edad;
                    let total = [], ageRange = [];
                    let participants = {
                        mParticipants: [],
                        fParticipants: []
                    };

                    data.forEach((data) => {
                        total.push(0);

                        ageRange.push(data.type);
                        let m = data.f;
                        let f = data.m;

                        if (m !== undefined) {
                            participants.mParticipants.push(m);
                        } else {
                            participants.mParticipants.push(0);
                        }

                        if (f !== undefined) {
                            participants.fParticipants.push(f);
                        } else {
                            participants.fParticipants.push(0);
                        }
                    });

                    this.graphicAge(total, ageRange, participants);
                });

        },
        graphicAge(total, ageRange, participants) {
            const myChart = echarts.init(document.getElementById('AgeGraph'));

            const series = [
                {
                    name: 'Men',
                    itemStyle: {
                        color: this.colors.men
                    },
                    data: participants.fParticipants
                }, {
                    name: 'Women',
                    itemStyle: {
                        color: this.colors.women
                    },
                    data: participants.mParticipants
                }, {
                    name: 'total',
                    data: total
                }
            ];

            var genFormatter = (series, gender = null) => {
                return (param) => {
                    let sum = 0;
                    series.forEach(item => {
                        if (gender === null) {
                            sum += item.data[param.dataIndex];
                        } else if (item.name === this.names_legends[0] && gender === this.names_legends[0]) {
                            sum += item.data[param.dataIndex];
                        } else if (item.name === this.names_legends[1] && gender === this.names_legends[1]) {
                            sum += item.data[param.dataIndex];
                        } else if (gender === '') {
                            sum = 0;
                        }
                    });
                    return sum
                }
            };

            function isLastSeries(index) {
                return index === series.length - 1
            }

            var option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow' //'line' | 'shadow'
                    }, formatter: function (params) {
                        let axisValue = '<p>' + params[0].axisValue + '</p>';
                        params.forEach(item => {
                            if (item.seriesName !== 'total') {
                                axisValue += `<p>${item.marker} ${item.seriesName}:  ${item.data}</p>`;
                            }
                        });
                        return axisValue;
                    },
                },
                legend: {
                    data: this.names_legends,
                    center: 'right',
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                yAxis: {
                    type: 'value'
                },
                xAxis: {
                    type: 'category',
                    data: ageRange
                },
                series: series.map((item, index) => Object.assign(item, {
                    type: 'bar',
                    stack: true,
                    label: {
                        show: true,
                        formatter: isLastSeries(index) ? genFormatter(series) : null,
                        color: 'black',
                        position: isLastSeries(index) ? 'top' : 'inside'
                    },
                })),
                toolbox: this.setToolBox('Participants by Age')
            };

            myChart.setOption(option);
            this.responsiveChart('#tab_types-click', myChart);

            myChart.on('legendselectchanged', function (params) {

                let gender = null;
                let selected = params.selected;
                if (selected.Men && selected.Women) {
                    gender = null;
                } else if (!selected.Men && selected.Women) {
                    gender = this.names_legends[0];
                } else if (selected.Men && !selected.Women) {
                    gender = this.names_legends[1];
                } else {
                    gender = '';
                }

                option.series = series.map((item, index) => Object.assign(item, {
                    type: 'bar',
                    stack: true,
                    label: {
                        show: true,
                        formatter: isLastSeries(index) ? genFormatter(series, gender) : null,
                        color: 'black',
                        position: isLastSeries(index) ? 'top' : 'inside'
                    },
                }));

                myChart.setOption(option);
                this.responsiveChart('', myChart);
            })
        },
        graficoParticipantesEduacion() {
            $.post(UrlsAcciones.UrlGraficoEducacion, this.requestParameters)
                .then(response => {
                    let data = response.educacion;
                    let total = [], educations = [];
                    let participants = {
                        mParticipants: [],
                        fParticipants: []
                    };

                    data.forEach((data) => {
                        total.push(0);

                        educations.push(data.type);

                        let m = data.f;
                        let f = data.m;

                        if (m !== undefined) {
                            participants.mParticipants.push(m);
                        } else {
                            participants.mParticipants.push(0);
                        }

                        if (f !== undefined) {
                            participants.fParticipants.push(f);
                        } else {
                            participants.fParticipants.push(0);
                        }
                    });

                    this.graphicEducacion(total, educations, participants);
                });

        },
        graphicEducacion(total, ageRange, participants) {
            const myChart = echarts.init(document.getElementById('EducationGraph'));

            const series = [
                {
                    name: 'Men',
                    itemStyle: {
                        color: this.colors.men
                    },
                    data: participants.fParticipants
                },
                {
                    name: 'Women',
                    itemStyle: {
                        color: this.colors.women
                    },
                    data: participants.mParticipants
                },
                {
                    name: 'total',
                    data: total
                }
            ];

            function isLastSeries(index) {
                return index === series.length - 1
            }

            var option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow' //'line' | 'shadow'
                    }, formatter: function (params) {
                        let axisValue = `<p>${params[0].axisValue}</p>`;
                        params.forEach(item => {
                            if (item.seriesName !== 'total') {
                                axisValue += `<p>${item.marker} ${item.seriesName}: ${item.data}</p>`;
                            }
                        });
                        return axisValue;
                    },
                },
                legend: {
                    data: this.names_legends,
                    center: 'right',
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value'
                },
                yAxis: {
                    type: 'category',
                    data: ageRange,
                    axisLabel: {
                        verticalAlign: 'middle',
                    },
                },
                series: series.map((item, index) => Object.assign(item, {
                    type: 'bar',
                    stack: true,
                    label: {
                        show: true,
                        formatter: isLastSeries(index) ? this.genFormatter(series) : null,
                        color: 'black',
                        position: isLastSeries(index) ? 'right' : 'inside',
                        verticalAlign: 'middle',
                        distance: 35,
                    },
                })),
                toolbox: this.setToolBox('Participants by Education'),
            };
            this.responsiveChart('#tab_types-click', myChart);
            myChart.setOption(option);

            myChart.on('legendselectchanged', (params) => {

                let gender = null;
                let selected = params.selected;
                if (selected.Men && selected.Women) {
                    gender = null;
                } else if (!selected.Men && selected.Women) {
                    gender = this.names_legends[1];
                } else if (selected.Men && !selected.Women) {
                    gender = this.names_legends[0];
                } else {
                    gender = '';
                }

                option.series = series.map((item, index) => Object.assign(item, {
                    type: 'bar',
                    stack: true,
                    label: {
                        show: true,
                        formatter: isLastSeries(index) ? this.genFormatter(series, gender) : null,
                        color: 'black',
                        position: isLastSeries(index) ? 'right' : 'inside'
                    },

                }));
                this.responsiveChart('#tab_types-click', myChart);
                myChart.setOption(option);
            })
        },
        graficoParticipantesSexo() {

            let data = this.tatals;
            let total = data.T;

            let totalMen = {
                name: 'Men',
                value: data.M
            };

            let totalWomen = {
                name: 'Women',
                value: data.F
            };
            this.graphicSexo(total, totalMen, totalWomen);

        },
        graphicSexo(total, totalMen, totalWomen) {
            const myChart = echarts.init(document.getElementById('SexGraph'));

            const option = {
                toolbox: this.setToolBox('Data participants reached, by sex'),
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: this.names_legends
                },
                series: [
                    {
                        name: '',
                        type: 'pie',
                        radius: '35%',
                        center: ['50%', '50%'],
                        data: [{
                            name: totalMen.name,
                            value: totalMen.value,
                            itemStyle: {
                                color: this.colors.men
                            }
                        }, {
                            name: totalWomen.name,
                            value: totalWomen.value,
                            itemStyle: {
                                color: this.colors.women
                            }
                        }],
                        label: {
                            show: true,
                            formatter: function (params) {
                                return params.name + ': ' + params.percent + ' %, ' + params.value;
                            }
                        },
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };

            this.responsiveChart('#tab_types-click', myChart);
            myChart.setOption(option);
        },
        graphicGoalProject() {
            $.post(UrlsAcciones.UrlProjectGoal, this.requestParameters)
                .then(response => {
                    const chart_goal_project = echarts.init(document.getElementById('ProjectGoalsGraph'));
                    let data_project = response.proyectos_metas;
                    let data_chart = {
                        name_project: data_project['categorias'][0],
                        legends: [gettext('Participants'), gettext('Goals')],
                        legends_colors: [array_colors_lwr[0], array_colors_lwr[1]],
                        goals_data: [
                            data_project['series'][0]['data'][0],// goal men
                            data_project['series'][2]['data'][0],// goal women
                        ],
                        goals_color: [
                            data_project['series'][0]['color'],
                            data_project['series'][2]['color'],
                        ],
                        scope_data: [
                            data_project['data'][1].m,// scope men
                            data_project['data'][1].f,// scope women
                        ],
                        data_colors: [
                            data_project['series'][1]['color'],
                            data_project['series'][3]['color'],
                        ],
                        font_size: 16,
                    };


                    let option = {
                        toolbox: this.setToolBox('Total participants achieved and goals, by sex'),
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow'
                            }
                        },
                        legend: {
                            data: data_chart.legends,
                            top: '40',
                            icon: 'roundRect',
                            center: 'right',
                            color: data_chart.legends_colors,
                        },
                        xAxis: [{
                            show: true,
                            position: 'bottom',
                            name: gettext('Persons'),
                            nameLocation: 'middle',
                            nameGap: 30,
                        }],
                        yAxis: [{
                            show: true,
                            position: 'botton',
                            name: data_chart.name_project,
                            nameLocation: 'middle',
                            axisTick: 'none',
                            axisLabel: {
                                textStyle: {
                                    color: '#000',
                                    fontSize: data_project.font_size,
                                },
                            },
                            data: ['', '']
                        }, {
                            show: false,
                            axisTick: 'none',
                            axisLine: 'none',
                            axisLabel: {
                                textStyle: {
                                    color: '#000',
                                    fontSize: data_project.font_size,
                                },
                                margin: 30
                            },
                            data: this.names_legends
                        }, {
                            data: []
                        }],
                        series: [{
                            name: data_chart.legends[0],
                            type: 'bar',
                            data: data_chart.scope_data,
                            label: {
                                normal: {
                                    show: true,
                                    position: 'right',
                                    textStyle: {
                                        color: '#fff',
                                        fontSize: data_project.font_size,
                                    }
                                }
                            },
                            barWidth: 30,
                            itemStyle: {
                                normal: {
                                    color: function (params) {
                                        var num = data_chart.data_colors.length;
                                        return data_chart.data_colors[params.dataIndex % num]
                                    },
                                }
                            },
                            z: 2
                        }, {
                            name: data_chart.legends[1],
                            type: 'bar',
                            yAxisIndex: 1,
                            barGap: '-100%',
                            data: data_chart.goals_data,
                            barWidth: 60,
                            itemStyle: {
                                normal: {
                                    color: function (params) {
                                        var num = data_chart.goals_color.length;
                                        return data_chart.goals_color[params.dataIndex % num]
                                    },
                                }
                            },
                            z: 1
                        }]
                    };

                    chart_goal_project.setOption(option);
                    this.responsiveChart('', chart_goal_project);
                });
        },
        getGraphicZoom() {
            return [{
                "show": true,
                "height": 20,
                "xAxisIndex": [
                    0
                ],
                bottom: 30,
                "start": 30,
                "end": 100,
                handleIcon: this.icon_graph,
                handleSize: '110%',
                handleStyle: {
                    color: 'rgba(144,151,156,.8)',
                },
                textStyle: {
                    color: "#fff"
                },
                borderColor: "#90979c"
            }, {
                "type": "inside",
                "show": true,
                "height": 15,
                "start": 50,
                "end": 35
            }]
        },
        genFormatter(series, gender = null) {

            return (param) => {
                let sum = 0;
                series.forEach(item => {
                    if (gender === null) {
                        sum += item.data[param.dataIndex];
                    } else if (item.name === this.names_legends[0] && gender === this.names_legends[0]) {
                        sum += item.data[param.dataIndex];
                    } else if (item.name === this.names_legends[1] && gender === this.names_legends[1]) {
                        sum += item.data[param.dataIndex];
                    } else if (gender === '') {
                        sum = 0;
                    }
                });

                return sum
            }

        },
        formatAnioQuater(anioQuater) {
            let quater = anioQuater.split('Q');
            return quater[0] == 'None' ? '0000-Qn' : quater[0] + '-Q' + quater[1];
        },
        clearData() {
            /** Var gráfico participantes por año fiscal*/
            this.anios = [];
            this.hombres = [];
            this.mujeres = [];
            this.tatal = {};
            this.totalByBar = [];
            this.efauldSerie = [];
            this.metaPoranio = [];
            /** Var gráfico participantes quarter */
            this.aniosQ = [];
            this.hombresQ = [];
            this.mujeresQ = [];
            this.tatalsQ = {};
            this.totalByBarQ = [];
            this.defauldSerieQ = [];
        },
        responsiveChart(idtab, instance_echarts) {
            if (idtab.indexOf('.') > -1 || idtab.indexOf('#') > -1) {
                $(idtab).on('shown.bs.tab', function () {
                    instance_echarts.resize();
                });
            }

            window.onresize = function () {
                instance_echarts.resize();
            };
        },
        setToolBox(title_1) {
            return {
                show: true,
                feature: {
                    restore: {
                        title: gettext('Restore')
                    },
                    saveAsImage: {
                        title: gettext('Download as image')
                    },
                    dataView: {
                        title: gettext('Show data'),
                        readOnly: true,
                        lang: [gettext(title_1), gettext('Close'), gettext('Apply')]
                    },
                }
            }
        }
    },

};