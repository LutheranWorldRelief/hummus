let app = new Vue({
    el: "#app",
    mixins:[
        MergeUrls,
    ],
    data: {
        ids:[], // it is shown when the duplicate models were load
        name: '', // it is shown when the duplicate models were load
        loading: {
            all: true, // controls were duplicate models are loaded
            modal: true, // controls when to show the loading animation on the modal form
            fusion:false, // it indicates if the fusion process has been initialiced
            result:false,
        },
        modelFilter:{
            projectId:'',
            countryCode:'',
            organizationId:'',
        },
        modalState:'select', // stores the state of the modal view [select, resolve, fusion]
        modelsNames:[], // stores all the data from all the duplicate models by name
        models:[], // stores all the data from all the duplicate models by name
        modelSelected:null,
        modelCurrent:null,
        modelsResolve:{},
        modelLabels:{},
        modelEmpty:{},
        modelMerge:{}, // stores all the data from all the duplicate models by name
        list_organizations:{}, // stores the organizations listData ( id => name )
        list_projects:{}, // stores the projects listData ( id => name )
        list_types:{}, // stores the types data_list ( id => name ) values
        list_countries:{}, // stores the countries data_list ( id => name ) values
        list_education:{}, // stores the countries data_list ( id => name ) values

        noShowAttributes:[
            'id',
            'organizationName',
            'created',
            'modified',
            'errors',
        ],
        noShowFields:[
            'id',
            'country',
            'organization_id',
            'education_id',
            'type_id',
            'created',
            'modified',
            'errors',
        ],
        fusionResult:null,
        fusionFlags:{
            result:false
        },
        errorFlags:{
            fusion:false,
            finish:false,
        },
        errorMessage: {
            fusion:null,
            finish:null,
        },
    },
    methods: {
        load: function () {
            let self = this;
            self.loading.all = true;

            self.loadBaseUrl(self.$el);

            /* var modelFilter is global */
            if(typeof modelFilter !== 'undefined')
                self.modelFilter = modelFilter;

            /* var modelFilter is global */
            if(typeof gModels !== 'undefined')
                self.modelsNames = gModels;

            // ------------------------------------------------------------------------------ Getting label information
            $.get(self.getUrlModelLabels(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.modelLabels = data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar las etiquetas");
                    console.log("Error al cargar la información de los etiquetas");
                });

            // ------------------------------------------------------------------------------ Getting Empty Model
            $.get(self.getUrlModelEmpty(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.modelEmpty = data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar los datos de guardado");
                    console.log("Error al cargar la información del modelo vacío");
                });

            // ------------------------------------------------------------------------------ Getting Organization List
            $.get(self.getUrlOrganizations(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);

                self.list_organizations = data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar los datos de organizaciones");
                    console.log("Error al cargar la información de las organizaciones");
                });

            // ------------------------------------------------------------------------------ Getting Countries List
            $.get(self.getUrlCountries(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.list_countries = data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar los datos de los países");
                    console.log("Problema al cargar la información de los países");
                });

            // ------------------------------------------------------------------------------ Getting Projects List
            $.get(self.getUrlProjects(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.list_projects = data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar los datos de los proyectos");
                    console.log("Problema al cargar los datos de los proyectos");
                });

            // ------------------------------------------------------------------------------ Getting Types List
            $.get(self.getUrlTypes(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.list_types = data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar los datos de los tipos de beneficiarios");
                    console.log("Problema al cargar los datos de los tipos de beneficiarios");
                });

            // ------------------------------------------------------------------------------ Getting Types List
            $.get(self.getUrlEducation(), (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.list_education= data;
            })
                .fail(() => {
                    alertify.error("Problema al cargar el catalogo de tipo de educacion");
                    console.log("Problema al cargar el catalogo de tipo de educacion");
                });


        },
        removingFromDuplicateListImported:function(ids){
            let self = this;
            let indexes = [];

            let models = self.modelsNames.filter(function (model, index) {
                if (ids.indexOf(model.contact_id * 1) !== -1){
                    indexes.push(index);
                    return true;
                }
                return false;
            });

            console.log([models, ids, indexes, self.modelsNames]);

            $.each(models, function (index, model) {
                let i = self.modelsNames.indexOf(model);
                console.log(self.modelsNames.splice(i, 1));
            });
        },
        //----------------------------------------------------------------------------------------- MODAL URL FUNCTIONS
        fusionCancelar: function (modalName){
            let self = this;
            self.load.modal = false;
            self.load.fusion = false;
            switch (self.modalState){
                case 'resolve': self.modalState = 'select'; break;
                case 'fusion': self.modalState = 'resolve'; break;
                case 'finish':
                default:
                    $(modalName).modal('hide');
            }
        },
        fusionExclude: function (model) {
            let self = this;
            self.models.splice(self.models.indexOf(model), 1);
        },
        fusionSelect: function () {
            let self = this;
            self.loading.modal = true;
            self.modalState = 'resolve';
            self.ids = [];
            for (let i=0; i < self.models.length; i++){
                self.ids.push(self.models[i].id);
            }
            // ------------------------------------------------------------------------------ Getting Types List
            $.post(self.getUrlNameValues(), { ids: self.ids}, (data, textStatus, jqXHR) => {
                if(textStatus != 'success' ) console.log([textStatus, jqXHR]);
                self.modelMerge = data.values;
                let resolve = data.resolve;
                for(var attr in resolve){
                    self.modelMerge[attr] = resolve[attr][0];
                }
                self.modelsResolve = resolve;
                self.loading.modal = false;
            })
            .fail(() => {
                alertify.error("Problema al cargar los registros");
            });
        },
        fusionResolve: function () {
            let self = this;
            self.modalState = 'fusion';
        },
        fusionStart: function () {
            let self = this;
            self.loading.modal = true;
            self.loading.fusion = true;
            let data = {
                id: self.modelSelected,
                ids: self.ids,
                values: self.modelMerge,
            };

            // ------------------------------------------------------------------------------ Getting Types List
            $.post(self.getUrlFusion(), data, (data, textStatus, jqXHR) => {
                if(textStatus != 'success' )
                    console.log([textStatus, jqXHR]);
                else{
                    self.removingFromDuplicateListImported(self.ids);
                }
                self.fusionResult = data.result;
                self.fusionFlags.result = false;
                self.loading.modal = false;
                self.loading.fusion = false;
                self.modalState = 'finish';
            })
            .fail(() => {
                alertify.error("Problema al fusionar los registros de contacto.");

                self.loading.modal = false;
                self.loading.fusion = false;
            });
        },
        fusionFinish: function (){
            let self = this;
            if (self.modelCurrent)
            {
                // var index = self.modelsNames.indexOf(self.modelCurrent);
                // self.modelsNames.splice(index, 1);
                self.modelCurrent = null;
            }
        },
        //---------------------------------------------------------------------------------------------- PREPARING DATA
        showAttribute: function(field){
            let self = this;
            return self.noShowAttributes.indexOf(field) != -1 ? false : true;
        },
        showField: function(field){
            let self = this;
            return self.noShowFields.indexOf(field) != -1 ? false : true;
        },
        //---------------------------------------------------------------------------------------------- PREPARING DATA
        preparingFusionForm: function (model) {
            let self = this;

            self.ids = [];
            self.models = [];
            self.modelMerge = {};
            self.modelsResolve = {};
            self.modelSelected = null;
            self.fusionResult = null;
            self.fusionFlags.result = false;
            self.modelCurrent = model;

            self.loading.modal = true;
            self.name = model.contact_name;
            self.modalState = 'select';

            let url = self.getUrlId(model.contact_id);

            if (!url) {
                self.loading.modal = false;
                console.log("No se logró generar la URL para obtener la información del contacto");
            }
            else{
                $.get(url, (data, textStatus, jqXHR)=>{
                    if(textStatus !== 'success' ) console.log([textStatus, jqXHR]);

                    self.models = data.models;

                })
                    .fail(()=>{
                        console.log("No se logró generar la URL para obtener la información del contacto");
                    })
                    .always(() => {
                        self.loading.modal = false;
                    });
            }

            return false;
        }
    },
    mounted: function () {
        this.load();
    }
});