Vue.component('vue-multiselect', window.VueMultiselect.default);

var app = new Vue({
    el: '#app',
    mixins: [graphicMixins, geographicsMixins],
    data: {
        limit_options_countries: 9,//NOTE: change the value to vue change botons for multi-select
        limit_options_regions: 4,
        check_filter: false,
        // IMPORTANT NOTE: the keys of formInputs init with the values of variables from js in dashboard.html
        formInputs: {
            project_id: project_data,
            subproject_id: subproject,
            country_id: countries_data,
            lwrregion_id: regions_data,
            year: years_data,
            quarter: quarter,
            from_date: '',
            to_date: '',
            my_dashboard: my_dashboard,
        },
        requestParameters: {
            extra_counters: 1
        },
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
        btnClick: false,
        filterByUrl: false,
        currentUrl: null,
        parametersRequest: null,
        text_tooltip: 'Click to copy in clipboard',
        class_tabs_container: {
            'container-fluid': false,
            'tab-pane': false,
            'active': false,
            'fade': false,
            'show': false
        },
        data_subproject_graph: {
            target_data: [],
            actual_data: []
        },
        /** Var gráfico participantes por año fiscal*/
        anios: [], hombres: [], mujeres: [], tatals: {}, totalByBar: [], defauldSerie: [], targets_year: [],
        targets_women: [], targets_men: [],
        /** Var gráfico participantes quarter */
        aniosQ: [], hombresQ: [], mujeresQ: [], tatalsQ: {}, totalByBarQ: [], defauldSerieQ: [],
        show: true,
    },
    watch: {
        check_filter: function () {
            this.requestParameters = {
                extra_counters: 1
            };

            if (!this.filterByUrl) {
                this.formInputs.to_date = '';
                this.formInputs.from_date = '';
            }

            this.formInputs.quarter = null;
            this.formInputs.year = [];
            this.filterByUrl = false;
        },
        'formInputs.year': function (value) {
            if (value.length <= 0) {
                this.formInputs.quarter = null
            }
            this.loadDataWithFilters();
        },
        'formInputs.project_id': function () {
            if (this.formInputs.subproject_id) {
                this.formInputs.subproject_id = null;
            }

            $('#tab_quarter-click').children('li').eq(3).find('a').trigger('click');

            this.loadDataWithFilters();

            setTimeout(function () {
                $('#tab_quarter-click').children('li').eq(0).find('a').trigger('click');
            }, 1000);
        },
        'formInputs.subproject_id': function (value) {
            if (!value) {
                $('#tabs_projects-click').children('li').eq(0).find('a').trigger('click');
            }

            for (const key in this.class_tabs_container) {
                this.class_tabs_container[key] = (value !== null);
            }
            this.loadDataWithFilters();
        },
        'formInputs.country_id': function (values) {
            for (const item of this.list_countries) {
                item.active = values.some((country) => {
                    return item.value === country.value;
                });
            }
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
        },
    },
    created() {

        //NOTE Implementing localstorage browser for countries_polygon_json
        if (localStorage.getItem('countries_polygons_json')) {
            this.countries_polygons_json = JSON.parse(localStorage.getItem('countries_polygons_json'));
        } else {
            console.log(2);
            $.get(UrlsAcciones.UrlCountriesPolygons)
                .then(response => {
                    this.countries_polygons_json = response;
                    localStorage.setItem(
                        'countries_polygons_json', JSON.stringify(this.countries_polygons_json)
                    );
                });
        }


        // NOTE variable declare in monitoring/template/modular_admin/dashboard.html
        this.list_years = years;

        $.get(UrlsAcciones.UrlProjects)
            .then(projects => {
                this.list_projects = [];

                for (const id in projects) {
                    this.list_projects.push({
                        name: projects[id],
                        value: id
                    });
                }
            });

        this.loadDataWithFilters();

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
    },
    methods: {

        loadSubprojects() {
            let project_id = this.requestParameters['project_id'];
            // NOTE: new_url content example = http://localhost/api/subproject/project/1/
            let new_url = `/api/subprojects/project/${project_id}/`;

            $.get(new_url)
                .then(response => {
                    let data = response.object_list;
                    this.list_subprojects = [];
                    for (const subproject of data) {
                        this.list_subprojects.push({
                            name: subproject['name'],
                            value: subproject['id']
                        })
                    }
                });
        },
        loadDataWithFilters() {
            this.getValueOfFilter()
                .then(() => {
                    this.loadCatalogs();
                    this.loadCountriesMaps();
                    this.loadDataForDashboard();
                });
        },
        loadDataForDashboard() {

            if (this.formInputs.project_id) {
                //function to graph a Chart with Goal and Scope of Women and Men
                this.graphicGoalProject();
                this.loadSubprojects();
            }

            $.get(UrlsAcciones.UrlQuantitySubProjects, this.requestParameters)
                .then(response => {
                    this.quantity_subprojects = response.quantity_subprojects;
                });
            var contentVue = this
            $.get(UrlsAcciones.UrlTarget, this.requestParameters)
                .then(function (response) {

                    contentVue.createUrl(this.url);
                    let targets = response.totals;
                    let target_years = response.year;
                    //set the global target Total
                    contentVue.goal_participants = contentVue.setZero(targets.T);
                    //set the global target by gender in array
                    contentVue.data_subproject_graph.target_data = [];
                    contentVue.data_subproject_graph.target_data.push(
                        contentVue.setZero(targets.F),
                        contentVue.setZero(targets.M)
                    );
                    //set the targets(Total,Male & Female) by year
                    contentVue.targets_year = [];
                    for (const year in target_years) {
                        contentVue.targets_men.push(contentVue.setZero(target_years[year].M));
                        contentVue.targets_women.push(contentVue.setZero(target_years[year].F));
                        contentVue.targets_year.push(contentVue.setZero(target_years[year].T));
                    }
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
                    //set the quantity of participats by gender in array
                    this.data_subproject_graph.actual_data = [];
                    this.data_subproject_graph.actual_data.push(
                        this.setZero(this.tatals.F),
                        this.setZero(this.tatals.M)
                    );

                    if (this.formInputs.subproject_id) {
                        let subproject_name = this.formInputs.subproject_id.name;
                        this.graphicGoalSubproject(subproject_name);
                    }

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
                    if (this.mujeresQ.length <= 0) {
                        for (const year of this.list_years) {
                            this.mujeres.push(0);
                            this.mujeresQ.push(0);
                            this.hombres.push(0);
                            this.hombresQ.push(0);
                            this.defauldSerie.push(0);
                            this.defauldSerieQ.push(0);
                        }
                    }

                    this.graphicFiscalyear();
                    this.graphicParticipants('GraphicQuarter');
                    this.graficoMetas();
                    this.graphFixedColumnGender();
                    // function to graph a stacked chart with line
                    this.graphicStackedLine();
                    this.loadDataTable();
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

            $.get(UrlsAcciones.UrlQuantityProjects, this.requestParameters)
                .then(data => {
                    this.quantity_projects = data.quantity_projects;
                });

            $.get(UrlsAcciones.UrlCountries, this.requestParameters)
                .then(data => {
                    this.list_countries = [];
                    let countries = data['paises'];
                    this.quantity_countries = countries.length;

                    for (const key in countries) {
                        let estado = countries[key].active;

                        if (countries_data.length > 0) {
                            estado = countries_data.some(obj => obj.value === countries[key].id);
                        }

                        this.list_countries.push({
                            name: countries[key].name,
                            value: countries[key].id,
                            active: estado,
                            region: countries[key].region,
                            projects: countries[key].projects,
                            subprojects: countries[key].subprojects,
                        });
                    }
                    this.btnClick = false;
                    this.loadCountriesMaps();
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
                this.requestParameters = {
                    extra_counters: 1
                };

                for (const key in this.formInputs) {
                    let input = this.formInputs[key];

                    if (!this.empty(input) && input.constructor === Object) {
                        this.requestParameters[key] = input['value'];
                    } else if (!this.empty(input) && input.constructor === Array) {
                        if (input.length > 0) {
                            if (key === 'country_id' && this.list_countries.length <= 0) {
                                let countries_id = [];
                                for (const country of input) {
                                    countries_id.push(country['value']);
                                }
                                if (countries_id.length > 0) {
                                    this.requestParameters[key] = countries_id;
                                }
                            } else {
                                this.requestParameters[key] = input;
                            }
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
            this.btnClick = true;
            let list_items = this.list_countries;
            let actives_regions = [];

            if (type_register !== 'country') {
                list_items = this.list_lwrregions;
            }

            register.active = !register.active;

            list_items.find((item) => {
                if (item.active) {
                    actives_regions.push(item.value);
                }
                if (type_register === 'country') {
                    countries_data = countries_data.filter((value) => {
                        return value !== item.value;
                    });

                    let country_index_exists = this.formInputs.country_id.findIndex(obj => obj.value === register.value);
                    if (country_index_exists >= 0) {
                        this.formInputs.country_id.splice(country_index_exists, 1);
                    } else {
                        this.formInputs.country_id.push({
                            name: register.name,
                            value: register.value,
                        });
                    }
                }
            });

            if (type_register !== 'country') {
                this.list_countries.forEach((row) => {
                    if (row.active && !actives_regions.includes(row.region)) {
                        row.active = !row.active;
                    }
                });
                this.loadDataWithFilters();
            }
        },
        createUrl(uri) {
            let uriRequest = decodeURI(uri);
            let parametersRequest = uriRequest.split('?');
            this.parametersRequest = parametersRequest[1];

            let urlBase = window.location.origin;

            if (parametersRequest.length > 1)
                this.currentUrl = urlBase + '/?' + parametersRequest[1];
            else
                this.currentUrl = urlBase;
        },
        clearFilters() {
            for (const key in this.formInputs) {
                if (key === 'my_dashboard')
                    continue;

                let type = typeof this.formInputs[key];
                switch (type) {
                    case 'object':
                        if (Array.isArray(this.formInputs[key])) {
                            this.formInputs[key] = []
                        } else {
                            this.formInputs[key] = null;
                        }
                        break;
                    case 'string':
                        this.formInputs[key] = '';
                        break;
                    case 'boolean':
                        this.formInputs[key] = false;
                        break;
                    default:
                }
            }
            this.requestParameters = {
                extra_counters: 1
            };

            this.list_countries.forEach((country) => {
                country.active = false
            });

            this.list_lwrregions.forEach((region) => {
                region.active = false
            });

            countries_data = [];
            project_data = null;
            subproject = null;
            regions_data = [];
            years_data = [];
            quarter = null;
        },
        setZero(data) {
            if (data === null)
                return 0;
            if (data === undefined)
                return 0;

            return data
        },
        copyLink() {
            let copyURL = document.getElementById('urlCopy');

            copyURL.select();
            copyURL.setSelectionRange(0, 99999);
            document.execCommand("copy");
        },
        loadDataTable() {
            $('#subprojectstable').DataTable({
                "ajax": "/api/subprojects/?" + this.parametersRequest,
                'destroy': true,
                'stateSave': true,
                "columns": [
                    {"data": "name"},
                    {"data": "country_id"},
                    {"data": "start"},
                    {"data": "end"},
                    {"data": "participants.totals.T"},
                    {"data": "targets"}
                ]
            });
        },
        changeStatusSwitchButton() {
            this.formInputs.my_dashboard = !this.formInputs.my_dashboard;
            if (this.formInputs.my_dashboard) {
                let switch_button = document.getElementById('change_url');
                window.location.href = switch_button.getAttribute('data-uri');
            } else {
                window.location.href = window.location.origin
            }
        }
    }
});
