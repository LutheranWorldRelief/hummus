var graphicMixins = {
    data() {
        return {
            typeGraphic: null
        }
    },
    methods: {
        graphicParticipats(type) {
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
                        name: 'Woman',
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

                option = {
                    color: ['#006699', '#e5323e'],
                    backgroundColor: '#f7f7ff',
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow' //'line' | 'shadow'
                        }, formatter: function (params) {
                            let axisValue = '<p>' + params[0].axisValue + '</p>';
                            params.forEach(item => {
                                if (item.seriesName != 'null')
                                    axisValue += '<p>' + item.marker + ' ' + item.seriesName + ': ' + item.data + '</p>';
                            });
                            return axisValue;
                        },
                    },
                    legend: {
                        data: ['Men', 'Woman'],
                        x: '50%',
                        top: '6%',
                        align: 'right',
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '6%',
                        containLabel: true
                    },
                    "calculable": true,
                    xAxis: [
                        {
                            type: 'category',
                            position: 'bottom',
                            data: type === 'GraphicQuarter' ? this.aniosQ : this.anios,
                            axisLabel: {
                                rotate: 90,
                                verticalAlign: 'middle',
                                //distance: 30,
                                //formatter: '{value} °C'
                            },
                            /*name: 'Participants by fiscal year',
                            fontSize: 18,
                            nameLocation: 'middle',
                            nameGap: 35,*/
                        }
                    ],
                    yAxis: {
                        type: 'value'
                    }, //Barra para realizar Zoom
                    "dataZoom": [{
                        "show": true,
                        "height": 20,
                        "xAxisIndex": [
                            0
                        ],
                        bottom: 0,
                        "start": 50,
                        "end": 100,
                        handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                        handleSize: '110%',
                        //backgroundColor:'rgba(51,255,204,.8)',
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
                    }], //Sumar valores de la serie (cantidad hombres y mujeres por año)
                    series: series.map((item, index) => Object.assign(item, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series) : null,
                            fontSize: isLastSeries(index) ? 13 : 11,
                            color: isLastSeries(index) ? '#4f5f6f' : '#fff',
                            position: isLastSeries(index) ? 'top' : 'inside',
                            /* position: 'top',*/
                            rotate: 90,
                            verticalAlign: 'middle',
                            distance: 30,
                        },
                    })),
                    title: {
                        text: type === 'GraphicQuarter' ? gettext('Participants by quarter') : gettext('Participants by fiscal year'),
                        x: 'center',
                        textStyle: {
                            fontWeight: 'bold',
                            color: '#b2bb1e',
                            paddingLeft: '3%'
                        }
                    }
                };
                myChart.setOption(option);

                resolved(true);
            });
        },//========================================================================================================
        graficoMetas() {

            let myChart = echarts.init(document.getElementById('MetaParticipantes'));

            /**
             * TODO
             * Inicio Asignanar meta
             * */
            var meta = [];
            this.totalByBar.forEach(function (numero, index) {
                if (Math.floor(Math.random() * 10) % 2 === 0)
                    meta.push(numero + (index * 100))
                else if (numero < 200)
                    meta.push(numero + (300))
                else
                    meta.push(numero - (1000))
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
                    rotate: 90,
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
                backgroundColor: '#f7f7ff',
                title: {
                    text: gettext('Assigned goal - amound goal'),
                    textStyle: {
                        fontWeight: 'bold',
                        color: '#b2bb1e',
                        paddingLeft: '3%'
                    },
                    x: 'center',
                    y: '1',
                },
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
                    // formatter: '{b}<br />{a0}: {c0}%<br />{a1}: {c1}%<br />{a2}: {c2}%',
                    formatter: function (params) {
                        let axisValue = '<p>' + params[0].axisValue + '</p>';
                        params.forEach(item => {
                            axisValue += '<p>' + item.marker + ' ' + item.seriesName + ': ' + item.data + '</p>';
                        });
                        return axisValue;
                    },
                    backgroundColor: 'rgba(0,0,0,0.7)',
                    padding: [6, 6],
                    extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);',
                },
                legend: {
                    //top: 30,
                    bottom: 'bottom',
                    textStyle: {
                        color: '#4f5f6f',
                    },

                    data: ['Actual', 'Meta'],
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
                },
                    {
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
                            //inside: false,
                            rotate: 270,
                            verticalAlign: 'middle',
                            textStyle: {
                                color: 'rgba(0,0,0,.6)',
                                fontSize: '11',
                                fontWeight: '560',
                            }, margin: 20,
                        },
                        data: this.metaPoranio
                        /*nameLocation: 'middle',
                        nameGap: 35,*/
                    },
                    {
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
                series:
                    [
                        {
                            name: 'Actual',
                            type: 'bar',
                            stack: '1',
                            xAxisIndex: 0,
                            data: this.totalByBar,//data1,
                            label: label,
                            barGap: '-100%',
                            barWidth: '35   %', //22
                            itemStyle: {
                                normal: {
                                    color: 'rgba(51,255,204,.9)',
                                }
                            },
                            z: 2
                        },
                        {
                            name: 'Meta',
                            type: 'bar',
                            xAxisIndex: 2,
                            data: this.metaPoranio,//[data1[0], data1[1], data1[2], 353,1000,900, 1100,1200,400,700,1300,3200,200],
                            barWidth: '67%', //35
                            itemStyle: {
                                normal: {
                                    color: 'rgba(61,134,163,0.8)',//'#006699',
                                    barBorderRadius: 1,
                                }
                            },
                            z: 1
                        },
                    ]
            };
            myChart.setOption(option);
        },
        graficoMetasLinea() {

            let myChart = echarts.init(document.getElementById('MetaParticipantesPorSexo'));

            option = {
                backgroundColor: '#f7f7ff',
                title: {
                    text: gettext('Assigned goal - amound goal by sex'),
                    textStyle: {
                        fontWeight: 'bold',
                        color: '#b2bb1e',
                        paddingLeft: '3%'
                    },
                    x: 'center',
                    y: '1',
                },
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
                    "data": ['Men', 'Woman', 'Meta']
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
                    "name": "Men",
                    "type": "bar",
                    "stack": "总量",
                    "barMaxWidth": 35,
                    "barGap": "20%",
                    "itemStyle": {
                        "normal": {
                            "color": "rgba(0,102,153,1)",
                            "label": {
                                "show": true,
                                "position": "inside",
                                color: '#fff',
                                fontWeight: '550',
                                fontSize: '11', //insideTop
                                formatter: function (p) {
                                    return p.value > 0 ? (p.value) : '';
                                }
                            }
                        }
                    },
                    "data": this.hombres
                },
                    {
                        "name": "Woman",
                        "type": "bar",
                        "stack": "总量",
                        "itemStyle": {
                            "normal": {
                                "color": "rgba(229,50,62,1)",
                                "barBorderRadius": 0,
                                "label": {
                                    "show": true,
                                    "position": "inside",
                                    color: '#fff',
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
                        "name": "Meta",
                        "type": "line",
                        "stack": true,
                        symbolSize: 10,
                        position: 'fixed',
                        symbol: 'circle',
                        "itemStyle": {
                            "normal": {
                                "color": "rgba(0,191,183,1)",
                                "barBorderRadius": 0,
                                "label": {
                                    "show": true,
                                    "position": "top",
                                    fontWeight: '570',
                                    fontSize: '12',
                                    distance: 35,
                                    rotate: 90,
                                    formatter: function (p) {
                                        return p.value > 0 ? (p.value) : '';
                                    }
                                }
                            }
                        },
                        "data": this.metaPoranio
                    },
                ]
            }
            myChart.setOption(option);
            this.styleGraphic.position = 'fixed';
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

            myChart.title = 'PARTICIPANTS BY AGE';

            const colors = {
                men: '#b2bb1e',
                women: '#00aaa7'
            };

            const series = [
                {
                    name: 'Men',
                    itemStyle: {
                        color: colors.women
                    },
                    data: participants.fParticipants
                },
                {
                    name: 'Women',
                    itemStyle: {
                        color: colors.men
                    },
                    data: participants.mParticipants
                },
                {
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
                        } else if (item.name === 'Men' && gender === 'Men') {
                            sum += item.data[param.dataIndex];
                        } else if (item.name === 'Women' && gender === 'Women') {
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
                                axisValue += '<p>' + item.marker + ' ' + item.seriesName + ': ' + item.data + '</p>';
                            }
                        });
                        return axisValue;
                    },
                },
                legend: {
                    data: ['Men', 'Women']
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
                }))

            };

            myChart.setOption(option);

            myChart.on('legendselectchanged', function (params) {

                let gender = null;
                let selected = params.selected;
                if (selected.Men && selected.Women) {
                    gender = null;
                } else if (!selected.Men && selected.Women) {
                    gender = 'Women';
                } else if (selected.Men && !selected.Women) {
                    gender = 'Men';
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
            })
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
                handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
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
        genFormatter(series) {
            return (param) => {
                //return this.typeGraphic === 'GraphicQuarter' ? this.totalByBarQ[param.dataIndex] : this.totalByBar[param.dataIndex]

                let sum = 0;
                series.forEach(item => {
                    sum += item.data[param.dataIndex];
                });
                return sum;
            }
        },
        formatAnioQuater(anioQuater) {
            let quater = anioQuater.split('Q');
            return quater[0] == 'None' ? '0000-Qn' : quater[0] + '-Q' + quater[1];
        },
        showGraphicMetaSexo(option) {

            if (option == 1) {
                this.styleGraphic.position = 'relative'
            } else {
                this.styleGraphic.position = 'fixed'
            }
        }
    }
}