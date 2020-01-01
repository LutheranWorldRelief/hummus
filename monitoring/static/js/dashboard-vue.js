Vue.component('vue-multiselect', window.VueMultiselect.default);

var app = new Vue({
    el: '#app',
    mixins: [graphicMixins],
    data: {
        check_filter: false,
        formInputs: {
            project_id: null,
            subproject_id: null,
            country_id: [],
            lwrregion_id: null,
            year: null,
            quarter: [],
            from_date: '',
            to_date: '',
        },
        requestParameters: {
            paises_todos: true,
            rubros_todos: true,
        },
        show_project: false,
        list_projects: [],
        list_countries: [],
        list_lwrregions: [],
        list_subprojects: [],
        list_years: [],
        quantity_projects: 0,
        quantity_subprojects: 0,
        quantity_participants: 0,
        quantity_countries: 0,
        goal_participants: 0,
        goal_percentage: 0,
        width_progress_bar: {
            width: '0px'
        },
        /** Var gráfico participantes por año fiscal*/
        anios: [], hombres: [], mujeres: [], tatals: {}, totalByBar: [], defauldSerie: [], metaPoranio: [],
        /** Var gráfico participantes quarter */
        aniosQ: [], hombresQ: [], mujeresQ: [], tatalsQ: {}, totalByBarQ: [], defauldSerieQ: [],
        show: true,
    },
    watch: {
        check_filter: function () {
            this.requestParameters = {
                paises_todos: true,
                rubros_todos: true,
            };
            this.formInputs.to_date = '';
            this.formInputs.from_date = '';
        },
        'formInputs.year': function (value) {
            if (this.empty(value)) {
                this.formInputs.quarter = []
            }
        }
    },
    created() {
        // NOTE variable declare in monitoring/template/modular_admin/dashboard.html
        this.list_years = years;

        this.loadCatalogs();

        this.loadDataForDashboard();
    },
    methods: {
        loadDataWithFilters() {
            this.getValueOfFilter().then(() => this.loadDataForDashboard());
        },
        loadDataForDashboard() {

            this.show_project = !this.empty(this.requestParameters.project_id);

            $.post(UrlsAcciones.UrlDatosCantidadParticipantes, this.requestParameters)
                .then(((response) => {
                    this.quantity_participants = response.participantes;
                    // TODO set in goal_participants the global goal
                    this.goal_participants = 1000 + response.participantes;
                    this.goal_percentage = this.percentage(this.quantity_participants, this.goal_participants);
                    this.width_progress_bar.width = this.goal_percentage + '%';
                }));

            if (this.show_project) {
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

            $.get(UrlsAcciones.UrlDatosGraficosParticipantes, this.requestParameters)
                .then(((response) => {
                    this.clearData();
                    let data = response;

                    this.tatals = data['totals'];
                    delete data.totals;

                    // funcion to graph the participants by sex
                    this.graficoParticipantesSexo();

                    setZeroIsUndefined = (data) => {
                        return data === undefined ? 0 : data
                    };
                    /** Recorrer participantes por anio fisca */
                    for (const participants in data['year']) {
                        this.anios.push(participants);
                        this.totalByBar.push(setZeroIsUndefined(data['year'][participants].T));
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

                    this.graphicParticipants('').then(() => {
                        this.graphicParticipants('GraphicQuarter');
                        this.graficoMetas();
                        this.graficoMetasLinea();
                    });

                }));
            // funcion to graph the participants by age
            this.graficoParticipantesEdad();
            // funcion to graph the participants by education
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
            if (!this.empty(this.formInputs.project_id)) {
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
            }
            $.get(UrlsAcciones.UrlCountries, this.requestParameters)
                .then(data => {
                    this.list_countries = [];
                    let countries = data['paises'];
                    this.quantity_countries = countries.length;
                    for (const key in countries) {
                        this.list_countries.push({
                            name: countries[key].name,
                            value: countries[key].id,
                            active: countries[key].active,
                        });
                    }
                });

            $.get(UrlsAcciones.UrlLWRregions, this.requestParameters)
                .then(data => {
                    this.list_lwrregions = [];
                    let regions = data['regions'];
                    for (const key in regions) {
                        this.list_lwrregions.push({
                            name: regions[key].name,
                            value: regions[key].id,
                            active: regions[key].active
                        });
                    }
                });
        },
        getValueOfFilter() {
            return new Promise((resolved, reject) => {
                for (const key in this.formInputs) {
                    let input = this.formInputs[key];

                    if (!this.empty(input) && input.constructor === Object) {
                        this.requestParameters[key] = input['value'];
                    } else if (!this.empty(input) && input.constructor === Array) {
                        if (input.length > 0) {
                            this.requestParameters[key] = input;
                        }
                    } else if (!this.empty(input)) {
                        this.requestParameters[key] = input;
                    }
                }

                this.getSelectedCountriesRegions();
                resolved(true);
            })
        },
        getSelectedCountriesRegions() {

            let countries = [];
            for (const country of this.list_countries) {
                if (country.active)
                    countries.push(country.value);
            }

            if (countries.length > 0)
                this.requestParameters.country_id = countries;

            let lwr_regions = [];
            for (const region of this.list_lwrregions) {
                if (region.active)
                    lwr_regions.push(region.value)
            }

            if (lwr_regions.length > 0)
                this.requestParameters.lwrregion_id = lwr_regions
        },
        empty(data) {

            return data === '' || data == null || data === undefined;

        },
        changeActiveStatusAndFilter(register, type_register = 'country') {
            let list_items = [];

            if (type_register === 'country') {
                list_items = this.list_countries;
            } else {
                list_items = this.list_lwrregions;
            }

            for (const row of list_items) {
                if (row.name.toLowerCase() === register.name.toLowerCase()) {
                    row.active = !row.active;
                }
            }

            this.loadDataWithFilters();
            console.log(this.requestParameters.lwrregion_id);
            this.loadCatalogs();
        }

    }

});
