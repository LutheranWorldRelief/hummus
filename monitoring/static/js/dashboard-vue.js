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

            $.post(UrlsAcciones.UrlDatosCantidadProyectos, this.formInputs  )
                .then(((response) => {
                    this.quantity_projects = response.proyectos;
                }));

            $.post(UrlsAcciones.UrlDatosCantidadSubproyectos, this.formInputs   )
                .then(((response) => {
                    this.quantity_subprojects = response.subproyectos;
                }));

            $.post(UrlsAcciones.UrlDatosCantidadParticipantes, this.formInputs  )
                .then(((response) => {
                    this.quantity_participants = response.participantes;
                }));
        },
    }

});