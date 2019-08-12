// @ts-ignore
var app = new Vue({
    el: "#app",
    mixins: [
        // @ts-ignore
        MergeUrls,
    ],
    data: {
        ids: [],
        name: '',
        loading: {
            all: true,
            modal: true,
            fusion: false,
            result: false,
        },
        modelFilter: {
            projectId: '',
            countryCode: '',
            organizationId: '',
            nameSearch:''
        },
        modalState: 'select',
        modelsAll: [],
        models: [],
        modelSelected: null,
        modelsResolve: {},
        modelLabels: {},
        modelEmpty: {},
        modelMerge: {},
        list_organizations: {},
        list_projects: {},
        list_types: {},
        list_countries: {},
        list_education: {},
        noShowAttributes: [
            'id',
            'organizationName',
            'created',
            'modified',
            'errors',
        ],
        noShowFields: [
            'id',
            'country',
            'organization_id',
            'education_id',
            'type_id',
            'created',
            'modified',
            'errors',
        ],
        fusionResult: null,
        fusionFlags: {
            result: false
        },
        errorFlags: {
            fusion: false,
            finish: false,
        },
        errorMessage: {
            fusion: null,
            finish: null,
        },
    },
    methods: {
        load: function () {
            var self = this;
            self.loading.all = true;
            self.loadBaseUrl(self.$el);
            /* var modelFilter is global */
            // @ts-ignore
            if (typeof modelFilter !== 'undefined')
                // @ts-ignore
                self.modelFilter = modelFilter;
            // ------------------------------------------------------------------------------ Getting label information
            // @ts-ignore
            $.get(self.getUrlModelLabels(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelLabels = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar las etiquetas");
                console.log("Error al cargar la información de los etiquetas");
            });
            // ------------------------------------------------------------------------------ Getting Empty Model
            // @ts-ignore
            $.get(self.getUrlModelEmpty(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelEmpty = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar los datos de guardado");
                console.log("Error al cargar la información del modelo vacío");
            });
            // ------------------------------------------------------------------------------ Getting Organization List
            // @ts-ignore
            $.get(self.getUrlOrganizations(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_organizations = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar los datos de organizaciones");
                console.log("Error al cargar la información de las organizaciones");
            });
            // ------------------------------------------------------------------------------ Getting Countries List
            // @ts-ignore
            $.get(self.getUrlCountries(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_countries = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar los datos de los países");
                console.log("Problema al cargar la información de los países");
            });
            // ------------------------------------------------------------------------------ Getting Projects List
            // @ts-ignore
            $.get(self.getUrlProjects(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_projects = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar los datos de los proyectos");
                console.log("Problema al cargar los datos de los proyectos");
            });
            // ------------------------------------------------------------------------------ Getting Types List
            // @ts-ignore
            $.get(self.getUrlTypes(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_types = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar los datos de los tipos de beneficiarios");
                console.log("Problema al cargar los datos de los tipos de beneficiarios");
            });
            // ------------------------------------------------------------------------------ Getting Types List
            // @ts-ignore
            $.get(self.getUrlEducation(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_education = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar el catalogo de tipo de educacion");
                console.log("Problema al cargar el catalogo de tipo de educacion");
            });
            // ------------------------------------------------------------------------------ Getting Models
            // @ts-ignore
            $.get(self.getUrlAllDocs(), self.modelFilter, function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelsAll = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al ");
                console.log("Error al cargar la información de los contactos");
            })
                .always(function () {
                self.loading.all = false;
            });
        },
        loadModels: function () {
            var self = this;
            self.loading.all = true;
            // @ts-ignore
            $.get(self.getUrlAllDocs(), self.modelFilter, function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelsAll = data;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al ");
                console.log("Error al cargar la información de los contactos");
            })
                .always(function () {
                self.loading.all = false;
            });
        },
        //----------------------------------------------------------------------------------------- MODAL URL FUNCTIONS
        fusionCancelar: function (modalName) {
            var self = this;
            self.load.modal = false;
            self.load.fusion = false;
            switch (self.modalState) {
                case 'resolve':
                    self.modalState = 'select';
                    break;
                case 'fusion':
                    self.modalState = 'resolve';
                    break;
                case 'finish':
                default:
                    // @ts-ignore
                    $(modalName).modal('hide');
            }
        },
        fusionExclude: function (model) {
            var self = this;
            self.models.splice(self.models.indexOf(model), 1);
        },
        fusionSelect: function () {
            var self = this;
            self.loading.modal = true;
            self.modalState = 'resolve';
            self.ids = [];
            for (var i = 0; i < self.models.length; i++) {
                self.ids.push(self.models[i].id);
            }
            // ------------------------------------------------------------------------------ Getting Types List
            // @ts-ignore
            $.post(self.getUrlDocValues(), { ids: self.ids }, function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelMerge = data.values;
                var resolve = data.resolve;
                for (var attr in resolve) {
                    self.modelMerge[attr] = resolve[attr][0];
                }
                self.modelsResolve = resolve;
                self.loading.modal = false;
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al cargar los registros");
            });
        },
        fusionResolve: function () {
            var self = this;
            self.modalState = 'fusion';
        },
        fusionStart: function () {
            var self = this;
            self.loading.modal = true;
            self.loading.fusion = true;
            var data = {
                id: self.modelSelected,
                ids: self.ids,
                values: self.modelMerge,
            };
            // ------------------------------------------------------------------------------ Getting Types List
            // @ts-ignore
            $.post(self.getUrlFusion(), data, function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.fusionResult = data.result;
                self.fusionFlags.result = false;
                self.loading.modal = false;
                self.loading.fusion = false;
                self.modalState = 'finish';
            })
                .fail(function () {
                // @ts-ignore
                alertify.error("Problema al fusionar los registros de contacto.");
                self.loading.modal = false;
                self.loading.fusion = false;
            });
        },
        fusionFinish: function () {
            var self = this;
            self.load();
        },
        //---------------------------------------------------------------------------------------------- PREPARING DATA
        showAttribute: function (field) {
            var self = this;
            return self.noShowAttributes.indexOf(field) != -1 ? false : true;
        },
        showField: function (field) {
            var self = this;
            return self.noShowFields.indexOf(field) != -1 ? false : true;
        },
        //---------------------------------------------------------------------------------------------- PREPARING DATA
        preparingFusionForm: function (model) {
            var self = this;
            self.ids = [];
            self.models = [];
            self.modelMerge = {};
            self.modelsResolve = {};
            self.modelSelected = null;
            self.fusionResult = null;
            self.fusionFlags.result = false;
            self.loading.modal = true;
            self.name = model.document;
            self.modalState = 'select';
            var url = self.getUrlDoc(self.name);
            if (!url) {
                self.loading.modal = false;
                console.log("No se logró generar la URL para obtener la información del contacto");
            }
            else {
                // @ts-ignore
                $.get(url, function (data, textStatus, jqXHR) {
                    if (textStatus !== 'success')
                        console.log([textStatus, jqXHR]);
                    self.models = data.models;
                })
                    .fail(function () {
                    console.log("No se logró generar la URL para obtener la información del contacto");
                })
                    .always(function () {
                    self.loading.modal = false;
                });
            }
            return false;
        },
        btnFiltrarClick: function () {
            var self = this;
            self.loadModels();
        },
        btnLimpiarFiltroClick: function () {
            var self = this;
            self.modelFilter.nameSearch = '';
            self.loadModels();
        }
    },
    mounted: function () {
        this.load();
    }
});
