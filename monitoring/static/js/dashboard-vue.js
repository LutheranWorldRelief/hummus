Vue.component('vue-multiselect', window.VueMultiselect.default);

var app = new Vue({
    el: '#app',
    data: {
        formInputs: {
            project: {},
            country: {},
            lwrregion: '',
            year: '',
        },
        requestParameters: {
            project_id: '',
            paises_todos: true,
            rubros_todos: true,
            from_date: '',
            to_date: '',
            country_id: [],
            lwrregion_id: '',
            year: '',
        },
        hide_project: false,
        list_projects: [],
        list_countries: [],
        quantity_projects: 0,
        quantity_subprojects: 0,
        quantity_participants: 0,
    },
    created() {
        $.get(UrlsAcciones.UrlProjects)
            .then(data => {
                this.quantity_projects = Object.keys(data).length;
                for (const key in data) {
                    this.list_projects.push({
                        name: data[key],
                        value: key
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

        this.loadDataForDashboard();
    },
    methods: {
        loadDataForDashboard() {

            if (this.formInputs.project['value']) {
                this.hide_project = true;
                this.requestParameters.project_id = this.formInputs.project['value'];
            }

            this.requestParameters.lwrregion_id = this.formInputs.lwrregion;
            this.requestParameters.country_id = this.formInputs.country;

            $.post(UrlsAcciones.UrlDatosCantidadParticipantes, this.requestParameters)
                .then(((response) => {
                    this.quantity_participants = response.participantes;
                }));

            if (this.requestParameters.project_id !== '') {
                console.log(this.requestParameters.project_id);
                //new_url content; example = http://localhost/api/subproject/project/1/
                let new_url = `api/subprojects/project/${this.requestParameters.project_id}/`;

                $.get(new_url)
                    .then(response => {
                        this.quantity_subprojects = response.object_list.length;
                    });
            } else {
                $.get(UrlsAcciones.UrlSubProjects)
                    .then(response => {
                        this.quantity_subprojects = response.object_list.length;
                    });
            }
        },
    }

});