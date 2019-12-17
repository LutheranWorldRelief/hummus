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
        axios.post(UrlsAcciones.UrlDatosCantidadProyectos, this.convertToFormdata())
            .then(((response) => {
                let data = response.data;
                this.quantity_projects = data.proyectos;
            }));
    },
    methods: {
        convertToFormdata() {
            let form_data = new FormData();
            for (let key of Object.keys(this.formInputs)) {
                form_data.append(key, this.formInputs[key]);
            }
            return form_data;
        }
    }

});