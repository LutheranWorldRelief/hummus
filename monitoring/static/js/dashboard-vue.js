var app = new Vue({
    el: '#app',
    data: {
        formInputs: {
            proyecto: '',
            paises_todos: true,
            rubros_todos: true,
            desde: '',
            hasta: '',
            paises: [],
        },
        quantity_projects: 0,
        quantity_subprojects: 0,
        quantity_participants: 0,
    },
    mounted() {
        this.loadDataForDashboard();
    },
    methods: {
        loadDataForDashboard() {
            let data_input = this.convertToFormdata();

            axios
                .post(UrlsAcciones.UrlDatosCantidadProyectos, data_input)
                .then(((response) => {
                    let data = response.data;
                    this.quantity_projects = data.proyectos;
                }));

            axios
                .post(UrlsAcciones.UrlDatosCantidadSubproyectos, data_input)
                .then(((response) => {
                    let data = response.data;
                    this.quantity_subprojects = data.subproyectos;
                }));

            axios
                .post(UrlsAcciones.UrlDatosCantidadParticipantes, data_input)
                .then(((response) => {
                    let data = response.data;
                    this.quantity_participants = data.participantes;
                }));
        },
        convertToFormdata() {
            let form_data = new FormData();
            for (let key of Object.keys(this.formInputs)) {
                form_data.append(key, this.formInputs[key]);
            }
            return form_data;
        }
    }

});