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
        quantity_subprojects: 0
    },
    mounted() {
        this.loadDataForDashboard();
    },
    methods: {
        loadDataForDashboard() {
            axios
                .post(UrlsAcciones.UrlDatosCantidadProyectos, this.convertToFormdata())
                .then(((response) => {
                    let data = response.data;
                    this.quantity_projects = data.proyectos;
                }));

            axios
                .post(UrlsAcciones.UrlDatosCantidadSubproyectos, this.convertToFormdata())
                .then(((response) => {
                    let data = response.data;
                    this.quantity_subprojects = data.subproyectos;
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