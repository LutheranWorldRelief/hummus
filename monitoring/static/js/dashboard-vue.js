Vue.component('vue-multiselect', window.VueMultiselect.default);

var app = new Vue({
    el: '#app',
    mixins: [graphicMixins],
    data: {
        formInputs: {
            project: {},
            subproject: {},
            country: {},
            lwrregion: '',
            year: '',
            quarter: '',
        },
        requestParameters: {
            project_id: '',
            subproject_id: '',
            paises_todos: true,
            rubros_todos: true,
            from_date: '',
            to_date: '',
            country_id: [],
            lwrregion_id: '',
            year: '',
            quarter: '',
        },
        hide_project: false,
        list_projects: [],
        list_countries: [],
        list_lwrregions: [],
        list_subprojects: [],
        quantity_projects: 0,
        quantity_subprojects: 0,
        quantity_participants: 0,
        goal_participants: 0,
        goal_percentage: 0,
        width_progress_bar: {
            width: '0px'
        },
        /** Var gráfico participantes por año fiscal*/
        anios: [], hombres: [], mujeres: [], tatals: {}, totalByBar: [], defauldSerie: [], metaPoranio: [],
        /** Var gráfico participantes quarter */
        aniosQ: [], hombresQ: [], mujeresQ: [], tatalsQ: {}, totalByBarQ: [], defauldSerieQ: [],
        show: true, styleGraphic: {
            position: '',
            height: '500px'
        }
    },
    created() {
        this.loadCatalogs();

        this.loadDataForDashboard();
    },
    methods: {
        loadDataForDashboard() {

            if (this.formInputs.project['value']) {
                this.hide_project = true;
                this.requestParameters.project_id = this.formInputs.project['value'];
            } else {
                this.hide_project = false;
            }

            this.requestParameters.lwrregion_id = this.formInputs.lwrregion;
            this.requestParameters.country_id = this.formInputs.country;

            $.post(UrlsAcciones.UrlDatosCantidadParticipantes, this.requestParameters)
                .then(((response) => {
                    this.quantity_participants = response.participantes;
                    // TODO set in goal_participants the global goal
                    this.goal_participants = 1000 + response.participantes;
                    this.goal_percentage = this.percentage(this.quantity_participants, this.goal_participants);
                    this.width_progress_bar.width = this.goal_percentage + '%';
                }));

            if (this.requestParameters.project_id !== '') {
                // NOTE: new_url content example = http://localhost/api/subproject/project/1/
                let new_url = `/api/subprojects/project/${this.requestParameters.project_id}/`;

                $.get(new_url)
                    .then(response => {
                        let data = response.object_list;
                        this.quantity_subprojects = data.length;
                        for (const subproject of data) {
                            this.list_subprojects.push({
                                name: subproject['name'],
                                value: subproject['id']
                            })
                        }
                    });
                //function to graph a Chart with Goal and Scope of Women and Men
                this.graphicGoalProject();
            } else {
                $.get(UrlsAcciones.UrlSubProjects)
                    .then(response => {
                        this.quantity_subprojects = response.object_list.length;
                    });
            }

            $.get(UrlsAcciones.UrlDatosGraficosParticipantes, this.formInputs)
                .then(((response) => {
                    let data = response;
                    this.tatals = data['totals'];
                    delete data.totals;

                    setZeroIsUndefined = (data) => {
                        return data === undefined ? 0 : data
                    };
                    /** Recorrer participantes por anio fisca */
                    for (const participants in data['year']) {
                        this.anios.push(participants);
                        this.totalByBar.push(setZeroIsUndefined(data['year'][participants].T))
                        this.mujeres.push(setZeroIsUndefined(data['year'][participants].F));
                        this.hombres.push(setZeroIsUndefined(data['year'][participants].M));
                        this.defauldSerie.push(0);
                    }

                    /** Recorrer participantes por trimestre (Quarter) */
                    const orderedQ = {};

                    Object.keys(data['quarters']).sort().forEach(function (key) {
                        orderedQ[key] = data['quarters'][key];
                    });

                    for (const participants in orderedQ) {
                        this.aniosQ.push(this.formatAnioQuater(participants));

                        this.totalByBarQ.push(setZeroIsUndefined(orderedQ[participants].T));
                        this.mujeresQ.push(setZeroIsUndefined(orderedQ[participants].F));
                        this.hombresQ.push(setZeroIsUndefined(orderedQ[participants].M));
                        this.defauldSerieQ.push(0);
                    }

                    this.graphicParticipats('').then(() => {
                        this.graphicParticipats('GraphicQuarter');
                        this.graficoMetas();
                        this.graficoMetasLinea();
                    });

                }));
            // funcion to graph the quantity of participants by age
            this.graficoParticipantesEdad();
            // funcion to graph the quantity of participants by education
            this.graficoParticipantesEduacion();
        },
        percentage(dividend, divider) {
            if (dividend <= 0)
                return 0;

            if (divider <= 0)
                return 0;

            let percentage = (dividend / divider) * 100;

            return Math.round(percentage)

        },
        loadCatalogs() {
            $.get(UrlsAcciones.UrlProjects)
                .then(response => {
                    this.quantity_projects = response['object_list'].length;
                    let data = response['object_list'];

                    for (const key in data) {
                        this.list_projects.push({
                            name: data[key]['name'],
                            value: data[key]['id']
                        });
                    }
                });

            $.get(UrlsAcciones.UrlCountries)
                .then(data => {
                    for (const key in data) {
                        this.list_countries.push({
                            name: data[key],
                            value: key
                        });
                    }
                });

            $.get(UrlsAcciones.UrlLWRregions)
                .then(data => {
                    for (const key in data) {
                        this.list_lwrregions.push({
                            name: data[key],
                            value: key
                        });
                    }
                });
        }
    }

});
