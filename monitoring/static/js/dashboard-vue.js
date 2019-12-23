var app = new Vue({
    el: '#app',
    mixins: [graphicMixins],
    data: {
        formInputs: {
            proyecto: '',
            paises_todos: true,
            rubros_todos: true,
            desde: '',
            hasta: '',
            paises: []
        },
        quantity_projects: 0,
        quantity_subprojects: 0,
        quantity_participants: 0,
        /** Var gráfico participantes por año fiscal*/
        anios: [], hombres: [], mujeres: [], tatals: {}, totalByBar: [], defauldSerie: [],metaPoranio:[],
        /** Var gráfico participantes quarter */
        aniosQ: [], hombresQ: [], mujeresQ: [], tatalsQ: {}, totalByBarQ: [], defauldSerieQ: [],
        show:true, styleGraphic:{
            position:'',
            height:'500px'
        }
    },
    created() {
        this.loadDataForDashboard();
    },
    methods: {
        loadDataForDashboard() {

            $.post(UrlsAcciones.UrlDatosCantidadProyectos, this.formInputs)
                .then(((response) => {
                    this.quantity_projects = response.proyectos;
                }));

            $.post(UrlsAcciones.UrlDatosCantidadSubproyectos, this.formInputs)
                .then(((response) => {
                    this.quantity_subprojects = response.subproyectos;
                }));

            $.post(UrlsAcciones.UrlDatosCantidadParticipantes, this.formInputs)
                .then(((response) => {
                    this.quantity_participants = response.participantes;
                }));

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

                        this.totalByBarQ.push(setZeroIsUndefined(orderedQ[participants].T))
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
        },
    }

});