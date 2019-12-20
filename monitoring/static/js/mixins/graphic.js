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
                this.typeGraphic = type
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
                        bottom: 'bottom',
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '6%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type: 'category',
                            position: 'bottom',
                            data: type === 'GraphicQuarter' ? this.aniosQ : this.anios,
                            axisLabel: {
                                rotate: 90,
                                verticalAlign: 'middle',
                                /*distance: 19,*/
                                //formatter: '{value} °C'
                            },
                            //name: 'Participants by fiscal year',
                            fontSize: 18,
                            nameLocation: 'middle',
                            nameGap: 35,
                        }
                    ],
                    yAxis: {
                        type: 'value'
                    }, //Sumar valores de la serie (cantidad hombres y mujeres por año)
                    series: series.map((item, index) => Object.assign(item, {
                        type: 'bar',
                        stack: true,
                        label: {
                            show: true,
                            formatter: isLastSeries(index) ? this.genFormatter(series) : null,
                            fontSize: isLastSeries(index) ? 15 : 13,
                            color: 'black',
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
                            color: '#4f5f6f',
                            paddingLeft: '3%'
                        }
                    }
                };
                myChart.setOption(option);

                resolved(true);
            });
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
        }
    }
}