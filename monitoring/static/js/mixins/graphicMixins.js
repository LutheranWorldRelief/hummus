var graphicMixins = {
        data() {
            return {
                typeGraphic: null,
                background_color: '#fff',
                colors: {
                    men: array_colors_lwr[1],
                    target_men: array_colors_lwr[2],
                    women: array_colors_lwr[0],
                    target_women: array_colors_lwr[3],
                    target: array_colors_lwr[4],
                    actual: array_colors_lwr[5],
                },
                names_legends: [
                    gettext('Men'),
                    gettext('Women'),
                    gettext('Actual'),
                    gettext('Target'),
                ],
                label_participants: gettext('Participants'),
                label_project_subproject: {
                    normal: {
                        show: true,
                        position: 'right',
                        textStyle: {
                            color: '#000',
                            fontSize: 16,
                        },
                        formatter: (item) => {
                            return `${this.formatNumber(item.value)}`
                        }
                    }
                },
                icon_graph: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                radioSexPie: '70%',
            }
        },
        methods: {
            graphicFiscalyear() {
                let myChart = echarts.init(document.getElementById('FiscalYearGraph'));
                this.defaultSerie = new Array(this.hombres.length).fill(0);
                let series = [
                    {
                        name: this.names_legends[0],
                        type: 'bar',
                        stack: true,
                        label: {
                            normal: {
                                show: true,
                                position: 'insideRight'
                            }
                        },
                        data: this.hombres
                    },
                    {
                        name: this.names_legends[1],
                        type: 'bar',
                        stack: true,
                        label: {
                            normal: {
                                show: true,
                                position: 'insideRight'
                            }
                        },
                        data: this.mujeres
                    },
                    {
                        name: 'null',
                        data: this.defaultSerie
                    }
                ];

                function isLastSeries(index) {
                    return index === series.length - 1
                }

                let option = {
                    toolbox: this.setToolBox('Participants by fiscal year', true),
                    color: [this.colors.men, this.colors.women],
                    backgroundColor: this.background_color,
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow' //'line' | 'shadow'
                        }, formatter: (params) => {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                let datum = this.formatNumber(item.data);
                                if (item.seriesName !== 'null') {
                                    axisValue += `<p>${item.marker} ${item.seriesName}: ${datum}</p>`;
                                }
                            });
                            return axisValue;
                        },
                    },
                    legend: {
                        data: this.names_legends.slice(0, 2),
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
                        data: this.anios,
                        axisLabel: {
                            rotate: 90,
                            verticalAlign: 'middle',
                        },
                    }],
                    yAxis: {
                        type: 'value'
                    }, //Sumar valores de la serie (cantidad hombres y mujeres por año)
                    series: series.map((items, index) => Object.assign(items, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series) : this.getLocateStringChart(items, index),
                            fontSize: isLastSeries(index) ? 13 : 11,
                            color: isLastSeries(index) ? '#4f5f6f' : '#000',
                            position: isLastSeries(index) ? 'top' : 'inside',
                            verticalAlign: 'middle',
                            distance: 30,
                        },
                    }))
                };

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
                            formatter: isLastSeries(index) ? this.genFormatter(series, gender) : this.getLocateStringChart(items, index),
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
            },
            graphicParticipants(type) {
                return new Promise((resolved, reject) => {
                    let myChart = echarts.init(document.getElementById(type === 'GraphicQuarter' ? 'TrimestralGraph' : 'FiscalYearGraph'));

                    let series = [
                        {
                            name: this.names_legends[0],
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
                            name: this.names_legends[1],
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
                        toolbox: this.setToolBox(text_label, true),
                        color: [this.colors.men, this.colors.women],
                        backgroundColor: this.background_color,
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow' //'line' | 'shadow'
                            }, formatter: (params) => {
                                let axisValue = `<p>${params[0].axisValue}</p>`;
                                params.forEach(item => {
                                    let datum = this.formatNumber(item.data);
                                    if (item.seriesName !== 'null') {
                                        axisValue += `<p>${item.marker} ${item.seriesName}: ${datum}</p>`;
                                    }
                                });
                                return axisValue;
                            },
                        },
                        legend: {
                            data: this.names_legends.slice(0, 2),
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
                        series: series.map((items, index) => Object.assign(items, {
                            type: 'bar',
                            stack: true,
                            label: {
                                show: true,
                                formatter: isLastSeries(index) ? this.genFormatter(series) : this.getLocateStringChart(items, index),
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
                                formatter: isLastSeries(index) ? this.genFormatter(series, gender) : this.getLocateStringChart(items, index),
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

                var label = {
                    normal: {
                        show: true,
                        position: 'top',
                        distance: 15,
                        verticalAlign: 'middle',
                        formatter: (param) => {
                            return this.formatNumber(param.value);
                        },
                        textStyle: {
                            color: 'rgba(0,0,0,.7)',
                            fontSize: '11',
                            fontWeight: '560',
                        }
                    }
                };

                var option = {
                    toolbox: this.setToolBox('Actual vs Target'),
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
                        formatter: (params) => {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                axisValue += `<p>${item.marker} ${item.seriesName}: ${this.formatNumber(item.data)}</p>`;
                            });
                            return axisValue;
                        },
                        backgroundColor: 'rgba(0,0,0,0.7)',
                        padding: [6, 6],
                        extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);',
                    },
                    legend: {
                        bottom: 'bottom',
                        data: this.names_legends.slice(2, 4),
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
                        data: this.targets_year.map((item) => {
                            return this.formatNumber(item);
                        })
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
                        name: this.names_legends[2],
                        type: 'bar',
                        stack: '1',
                        xAxisIndex: 0,
                        data: this.totalByBar,
                        label: label,
                        barGap: '-100%',
                        barWidth: '35%',
                        itemStyle: {
                            normal: {
                                color: this.colors.actual,//actual
                            }
                        },
                        z: 2
                    }, {
                        name: this.names_legends[3],
                        type: 'bar',
                        xAxisIndex: 2,
                        data: this.targets_year,
                        barWidth: '67%',
                        itemStyle: {
                            normal: {
                                color: this.colors.target, //meta
                                barBorderRadius: 1,
                            }
                        },
                        z: 1
                    }]
                };
                this.responsiveChart('#tab_quarter-click', myChart);
                myChart.setOption(option);
            },
            graphFixedColumnGender() {
                let myChart = echarts.init(document.getElementById('FixedColumns'));

                let label = {
                    normal: {
                        show: true,
                        position: 'top',
                        distance: 15,
                        verticalAlign: 'middle',
                        formatter: function (param) {
                            return param.value;
                        },
                        textStyle: {
                            color: 'black',
                            fontSize: '11',

                        },
                        rotate: 90
                    }
                };

                let legends = [gettext('Woman'), gettext('Target Women'), gettext('Men'), gettext('Target Men')];

                let option = {
                    toolbox: this.setToolBox('Actual vs Target, by Sex(Fixed placement columns)'),
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
                        data: legends,
                        textStyle: {
                            color: '#4f5f6f',
                        },
                        bottom: 'bottom',
                    },
                    xAxis: {
                        boundaryGap: true,
                        axisLine: {
                            show: false
                        },
                        data: this.anios
                    },
                    yAxis: {
                        type: 'value',
                        axisLine: {
                            show: true,
                        }
                    },
                    series: [{
                        name: legends[0],
                        type: 'bar',
                        label: label,
                        barWidth: 8,
                        z: 10,
                        itemStyle: {
                            normal: {
                                color: this.colors.women
                            }
                        },
                        data: this.mujeres
                    }, {
                        name: legends[1],
                        type: 'bar',
                        barWidth: 20,
                        itemStyle: {
                            normal: {
                                color: this.colors.target_women
                            }
                        },
                        data: this.targets_women
                    }, {
                        name: legends[2],
                        type: 'bar',
                        barGap: '-175%',
                        label: label,
                        barWidth: 8,
                        z: 10,
                        itemStyle: {
                            normal: {
                                color: this.colors.men
                            }
                        },
                        data: this.hombres
                    }, {
                        name: legends[3],
                        type: 'bar',
                        barWidth: 20,
                        itemStyle: {
                            normal: {
                                color: this.colors.target_men
                            }
                        },
                        data: this.targets_men
                    }]
                };

                this.responsiveChart('#tabs_target-click', myChart);
                myChart.setOption(option);
            },
            graficoParticipantesEdad() {
                $.get(UrlsAcciones.UrlGraficoEdad, this.requestParameters)
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
                        name: this.names_legends[0],
                        itemStyle: {
                            color: this.colors.men
                        },
                        data: participants.fParticipants
                    }, {
                        name: this.names_legends[1],
                        itemStyle: {
                            color: this.colors.women
                        },
                        data: participants.mParticipants
                    }, {
                        name: gettext('total'),
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
                        return this.formatNumber(sum)
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
                        }, formatter: (params) => {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                if (item.seriesName !== 'total') {
                                    axisValue += `<p>${item.marker} ${item.seriesName}:  ${this.formatNumber(item.data)}</p>`;
                                }
                            });
                            return axisValue;
                        },
                    },
                    legend: {
                        data: this.names_legends.slice(0, 2),
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
                    series: series.map((items, index) => Object.assign(items, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? genFormatter(series) : this.getLocateStringChart(items, index),
                            color: 'black',
                            position: isLastSeries(index) ? 'top' : 'inside'
                        },
                    })),
                    toolbox: this.setToolBox('Participants by Age', true)
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
                            formatter: isLastSeries(index) ? genFormatter(series, gender) : this.getLocateStringChart(items, index),
                            color: 'black',
                            position: isLastSeries(index) ? 'top' : 'inside'
                        },
                    }));

                    myChart.setOption(option);
                    this.responsiveChart('', myChart);
                })
            },
            graficoParticipantesEduacion() {
                $.get(UrlsAcciones.UrlGraficoEducacion, this.requestParameters)
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
                        name: this.names_legends[0],
                        itemStyle: {
                            color: this.colors.men
                        },
                        data: participants.fParticipants
                    },
                    {
                        name: this.names_legends[1],
                        itemStyle: {
                            color: this.colors.women
                        },
                        data: participants.mParticipants
                    },
                    {
                        name: gettext('Total'),
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
                        }, formatter: (params) => {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                if (item.seriesName.toLowerCase() !== 'total') {
                                    axisValue += `<p>${item.marker} ${item.seriesName}: ${this.formatNumber(item.data)}</p>`;
                                }
                            });
                            return axisValue;
                        },
                    },
                    legend: {
                        data: this.names_legends.slice(0, 2),
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
                    series: series.map((items, index) => Object.assign(items, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series) : this.getLocateStringChart(items, index),
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

                    option.series = series.map((items, index) => Object.assign(items, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series, gender) : this.getLocateStringChart(items, index),
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
                let total = this.setZero(data.T);

                let totalMen = {
                    name: this.names_legends[0],
                    value: this.setZero(data.M)
                };

                let totalWomen = {
                    name: this.names_legends[1],
                    value: this.setZero(data.F)
                };
                this.graphicSexo(total, totalMen, totalWomen);
            },
            graphicSexo(total, totalMen, totalWomen) {
                const myChart = echarts.init(document.getElementById('SexGraph'));

                const option = {
                    toolbox: this.setToolBox('Data participants reached, by sex'),
                    tooltip: {
                        trigger: 'item',
                        formatter: (item) => {
                            console.log(item);
                            return `${item.name}: ${this.formatNumber(item.value)} (${item.percent}%)`
                        },
                    },
                    series: [{
                        name: '',
                        type: 'pie',
                        radius: this.radioSexPie,
                        center: ['50%', '50%'],
                        data: [{
                            name: totalMen.name,
                            value: totalMen.value,
                            itemStyle: {
                                color: this.colors.men
                            }, label: {
                                normal: {
                                    formatter: (item) => {
                                        return `${item.name}: ${this.formatNumber(item.value)} (${item.percent}%)`
                                    },
                                    position: 'inside'
                                }
                            }
                        }, {
                            name: totalWomen.name,
                            value: totalWomen.value,
                            itemStyle: {
                                color: this.colors.women
                            }, label: {
                                normal: {
                                    formatter: (item) => {
                                        return `${item.name}: ${this.formatNumber(item.value)} (${item.percent}%)`
                                    },
                                    position: 'inside'
                                }
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
                $.get(UrlsAcciones.UrlProjectGoal, this.requestParameters)
                    .then(response => {
                        const chart_goal_project = echarts.init(document.getElementById('ProjectGoalsGraph'));
                        let data_project = response.proyectos_metas;
                        let data_chart = {
                            name_project: data_project['categorias'][0],
                            legends: this.names_legends.slice(2, 4),
                            legends_colors: [this.colors.women, this.colors.men],
                            target_data: [
                                data_project['series'][0]['data'][0],// goal men
                                data_project['series'][2]['data'][0],// goal women
                            ],
                            scope_data: [
                                data_project['data'][1].m,// scope men
                                data_project['data'][1].f,// scope women
                            ],
                            font_size: 16,
                        };


                        let option = {
                            toolbox: this.setToolBox('Total actual participants and target, by sex'),
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
                                name: this.label_participants,
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
                                        fontSize: data_chart.font_size,
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
                                data: this.names_legends.slice(0, 2)
                            }, {
                                data: []
                            }],
                            series: [{
                                name: data_chart.legends[0],
                                type: 'bar',
                                data: data_chart.scope_data,
                                label: this.label_project_subproject,
                                barWidth: 30,
                                itemStyle: {
                                    normal: {
                                        color: data_chart.legends_colors[0]
                                    }
                                },
                                z: 2
                            }, {
                                name: data_chart.legends[1],
                                type: 'bar',
                                yAxisIndex: 1,
                                barGap: '-100%',
                                data: data_chart.target_data,
                                barWidth: 60,
                                itemStyle: {
                                    normal: {
                                        color: data_chart.legends_colors[1]
                                    }
                                },
                                z: 1
                            }]
                        };

                        chart_goal_project.setOption(option);
                        this.responsiveChart('#tabs_projects-click', chart_goal_project);
                    });
            },
            graphicGoalSubproject(name_subproject) {
                let chart_subproject = echarts.init(document.getElementById('SubprojectGoalsGraph'));
                let data_chart = {
                    name_project: name_subproject,
                    legends: this.names_legends.slice(2, 4).reverse(),
                    legends_colors: [this.colors.women, this.colors.men],
                    target_data: this.data_subproject_graph.target_data,
                    actual_data: this.data_subproject_graph.actual_data,
                    font_size: 16,
                };

                let option = {
                    toolbox: this.setToolBox(name_subproject),
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
                        name: this.label_participants,
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
                                fontSize: data_chart.font_size,
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
                                fontSize: data_chart.font_size,
                            },
                            margin: 30
                        },
                        data: this.names_legends.slice(0, 2)
                    }, {
                        data: []
                    }],
                    series: [{
                        name: data_chart.legends[0],
                        type: 'bar',
                        data: data_chart.actual_data,
                        label: this.label_project_subproject,
                        barWidth: 30,
                        itemStyle: {
                            normal: {
                                color: data_chart.legends_colors[0]
                            }
                        },
                        z: 2
                    }, {
                        name: data_chart.legends[1],
                        type: 'bar',
                        yAxisIndex: 1,
                        barGap: '-100%',
                        data: data_chart.target_data,
                        barWidth: 60,
                        itemStyle: {
                            normal: {
                                color: data_chart.legends_colors[1]
                            }
                        },
                        z: 1
                    }]
                };

                chart_subproject.setOption(option);
                this.responsiveChart('#tabs_projects-click', chart_subproject);
                setTimeout(function () {
                    $('#tabs_projects-click').children('li').eq(1).find('a').trigger('click');
                }, 500);
            },
            graphicStackedLine() {
                const myChart = echarts.init(document.getElementById('StackedLine'));

                const series = [{
                    name: this.names_legends[0],
                    type: 'bar',
                    stack: true,
                    label: {
                        show: true,
                        color: 'black',
                        position: 'inside',
                        formatter: (item) => {
                            return `${this.formatNumber(item.value)}`
                        }
                    },
                    itemStyle: {
                        color: this.colors.men
                    },
                    data: this.hombres
                }, {
                    name: this.names_legends[1],
                    type: 'bar',
                    stack: true,
                    label: {
                        show: true,
                        color: 'black',
                        position: 'inside',
                        formatter: (item) => {
                            return `${this.formatNumber(item.value)}`
                        }
                    },
                    itemStyle: {
                        color: this.colors.women
                    },
                    data: this.mujeres
                }, {
                    "name": gettext('Target'),
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
                                formatter: (p) => {
                                    return p.value > 0 ? this.formatNumber(p.value) : '';
                                }
                            }
                        }
                    },
                    "data": this.targets_year
                }];

                let option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow' //'line' | 'shadow'
                        }, formatter: (params) => {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                if (item.seriesName !== 'total') {
                                    axisValue += `<p>${item.marker} ${item.seriesName}:  ${this.formatNumber(item.data)}</p>`;
                                }
                            });
                            return axisValue;
                        },
                    },
                    legend: {
                        data: [
                            gettext('Men'),
                            gettext('Women'),
                            gettext('Target')],
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
                        data: this.anios
                    },
                    series: series
                };

                this.responsiveChart('#tab_quarter-click', myChart);
                myChart.setOption(option);
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

                    return this.formatNumber(sum)
                }
            },
            getLocateStringChart(items, index) {
                return (params) => {
                    return this.formatNumber(params.data);
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

                window.addEventListener('resize', function (event) {
                    let width = document.documentElement.clientWidth;
                    if (width >= 1700) {
                        this.radioSexPie = '70%';
                    } else if (width >= 1200 && width <= 1700) {
                        this.radioSexPie = '55%'
                    } else {
                        this.radioSexPie = '35%'
                    }
                });

                window.onresize = function () {
                    instance_echarts.resize();
                };
            },
            setToolBox(title_1, isCustomTable) {

                let tableData = {
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
                };
                if (isCustomTable)
                    Object.assign(tableData, this.customTable());

                return tableData;
            },
            customTable() {

                return {
                    optionToContent: function (opt) {

                        var axisData = opt.xAxis[0].data;
                        var series = opt.series;
                        var table = '<table style="width:70%; font-family: monospace; color:#000; font-size: 13px; font-weight:500; border: 1px solid #000;' +
                            '' +
                            '">' +
                            '<tbody></tbody> <tr>'
                            + '<td></td>'
                            + '<td>' + series[0].name + '</td>'
                            + '<td>' + series[1].name + '</td>'
                            + '</tr>';
                        for (var i = 0, l = axisData.length; i < l; i++) {
                            table += '<tr>'
                                + '<td>' + axisData[i] + '</td>'
                                + '<td>' + series[0].data[i] + '</td>'
                                + '<td>' + series[1].data[i] + '</td>'
                                + '</tr>';
                        }
                        table += '</tr></tbody></table>';

                        return table;
                    }
                }
            }
        },

    }
;
