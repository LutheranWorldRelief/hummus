Vue.component('vue-multiselect', window.VueMultiselect.default);

var app = new Vue({
    el: '#app',
    mixins: [graphicMixins, geographicsMixins],
    data: {
        check_filter: false,
        formInputs: {
            project_id: null,
            subproject_id: null,
            country_id: [],
            lwrregion_id: null,
            year: [],
            quarter: null,
            from_date: '',
            to_date: '',
        },
        requestParameters: {},
        show_projectgraph: false,
        show_subproject: false,
        spin_refresh_icon: false,
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
            this.requestParameters = {};
            this.formInputs.to_date = '';
            this.formInputs.from_date = '';
            this.formInputs.quarter = null;
            this.formInputs.year = [];
        },
        'formInputs.year': function (value) {
            if (value.length <= 0) {
                this.formInputs.quarter = null
            }
            this.loadDataWithFilters();
        },
        'formInputs.project_id': function (object) {
            this.show_subproject = (!this.empty(object));
            if (this.show_subproject) {
                let project_id = object.value;
                // NOTE: new_url content example = http://localhost/api/subproject/project/1/
                let new_url = `/api/subprojects/project/${project_id}/`;

                $.get(new_url)
                    .then(response => {
                        let data = response.object_list;
                        for (const subproject of data) {
                            this.list_subprojects.push({
                                name: subproject['name'],
                                value: subproject['id']
                            })
                        }
                    });
            }
            this.loadDataWithFilters();
        },
        'formInputs.subproject_id': function () {
            this.loadDataWithFilters();
        },
        'formInputs.country_id': function () {
            this.loadDataWithFilters();
        },
        'formInputs.lwrregion_id': function () {
            this.loadDataWithFilters();
        },
        'formInputs.quarter': function () {
            this.loadDataWithFilters();
        },
        'formInputs.from_date': function () {
            this.loadDataWithFilters();
        },
        'formInputs.to_date': function () {
            this.loadDataWithFilters();
        }
    },
    created() {
        // NOTE variable declare in monitoring/template/modular_admin/dashboard.html
        this.list_years = years;

        $.get(UrlsAcciones.UrlProjects)
            .then(projects => {
                this.list_projects = [];
                for (const id in projects){
                    this.list_projects.push({
                        name: projects[id],
                        value: id
                    });
                }
            });

        this.loadCatalogs();

        this.loadDataForDashboard();

        let width = document.documentElement.clientWidth;
        if (width >= 1700) {
            this.radioSexPie = '70%';
        } else if (width >= 1200 && width <= 1700) {
            this.radioSexPie = '60%'
        } else {
            this.radioSexPie = '50%'
        }

    },
    mounted() {
        this.$nextTick(function () {
            window.addEventListener('resize', function (event) {
                let width = document.documentElement.clientWidth;
                if (width >= 1700) {
                    this.radioSexPie = '70%';
                } else if (width >= 1200 && width <= 1700) {
                    this.radioSexPie = '60%'
                }
            });
        });
        this.loadCountriesMaps();
    },
    methods: {
        loadDataWithFilters() {
            this.getValueOfFilter()
                .then(() => {
                    this.loadCatalogs();
                    this.loadCountriesMaps();
                    this.loadDataForDashboard();
                });
        },
        loadDataForDashboard() {

            this.show_projectgraph = !this.empty(this.requestParameters.project_id);

            if (this.show_projectgraph) {
                //function to graph a Chart with Goal and Scope of Women and Men
                this.graphicGoalProject();
            }

            $.post(UrlsAcciones.UrlQuantitySubProjects, this.requestParameters)
                .then(response => {
                    this.quantity_subprojects = response.quantity_subprojects;
                });

            $.get(UrlsAcciones.UrlTarget, this.requestParameters)
                .then(response => {
                    let target = response.targets;
                    this.goal_participants = this.setZero(target.F) + this.setZero(target.M);
                });


            $.get(UrlsAcciones.UrlDatosGraficosParticipantes, this.requestParameters)
                .then(response => {
                    this.clearData();
                    let data = response;

                    this.tatals = data['totals'];
                    delete data.totals;

                    // funcion to graph the participants by sex
                    this.graficoParticipantesSexo();

                    /** Recorrer participantes por anio fisca */
                    for (const participants in data['year']) {
                        this.anios.push(participants);
                        this.totalByBar.push(this.setZero(data['year'][participants].T));
                        this.mujeres.push(this.setZero(data['year'][participants].F));
                        this.hombres.push(this.setZero(data['year'][participants].M));
                        this.defauldSerie.push(0);
                    }

                    //NOTE: calculating the number of participants
                    this.quantity_participants = this.setZero(this.tatals.T);
                    // calculating the percentage for the progress bar
                    this.goal_percentage = this.percentage(this.quantity_participants, this.goal_participants);
                    this.width_progress_bar.width = this.goal_percentage + '%';

                    /** Recorrer participantes por trimestre (Quarter) */
                    const orderedQ = {};

                    Object.keys(data['quarters']).sort().forEach(function (key) {
                        orderedQ[key] = data['quarters'][key];
                    });

                    for (const participants in orderedQ) {
                        this.aniosQ.push(this.formatAnioQuater(participants));
                        this.totalByBarQ.push(this.setZero(orderedQ[participants].T));
                        this.mujeresQ.push(this.setZero(orderedQ[participants].F));
                        this.hombresQ.push(this.setZero(orderedQ[participants].M));
                        this.defauldSerieQ.push(0);
                    }
                    // NOTE: mujeresQ is my pivot to verify is empty
                    //       to fill arrays with zeros
                    if (this.mujeresQ.length <= 0){
                        for (const year of this.list_years){
                            this.mujeres.push(0);
                            this.mujeresQ.push(0);
                            this.hombres.push(0);
                            this.hombresQ.push(0);
                            this.defauldSerie.push(0);
                            this.defauldSerieQ.push(0);
                        }
                    }

                    this.graphicParticipants('').then(() => {
                        this.graphicParticipants('GraphicQuarter');
                        this.graficoMetas();
                        this.graficoMetasLinea();
                    });

                });
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

            return percentage.toFixed(2);
        },
        loadCatalogs() {

            $.post(UrlsAcciones.UrlQuantityProjects, this.requestParameters)
                .then(data => {
                    this.quantity_projects = data.quantity_projects;
                });

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
                            region: countries[key].region,
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
                this.requestParameters = {};

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
            let list_items = this.list_countries;
            let actives_regions = [];

            if (type_register !== 'country') {
                list_items = this.list_lwrregions;
            }

            list_items.find(function (item) {
                if (item.name === register.name) {
                    item.active = !item.active
                }
                if (item.active) {
                    actives_regions.push(item.value);
                }
            });

            if (type_register !== 'country') {
                this.list_countries.find(function (row) {
                    if (row.active && !actives_regions.includes(row.region)) {
                        row.active = !row.active;
                    }
                })
            }

            this.loadDataWithFilters();
        },
        clearFilters() {
            this.formInputs = {
                project_id: null,
                subproject_id: null,
                country_id: [],
                lwrregion_id: null,
                year: [],
                quarter: null,
                from_date: '',
                to_date: '',
            };
            this.requestParameters = {};

            this.list_countries.forEach((country) => {
                country.active = false
            });

            this.list_lwrregions.forEach((region) => {
                region.active = false
            })

        },
        setZero(data) {
            if (data === null)
                return 0;
            if (data === undefined)
                return 0;

            return data
        }
    }
});
