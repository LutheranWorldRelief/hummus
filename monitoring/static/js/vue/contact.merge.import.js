var app = new Vue({
    el: "#app",
    mixins: [
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
        },
        modalState: 'select',
        modelsNames: [],
        models: [],
        modelSelected: null,
        modelCurrent: null,
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
            if (typeof modelFilter !== 'undefined')
                self.modelFilter = modelFilter;
            /* var modelFilter is global */
            if (typeof gModels !== 'undefined')
                self.modelsNames = gModels;
            // ------------------------------------------------------------------------------ Getting label information
            $.get(self.getUrlModelLabels(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelLabels = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar las etiquetas");
                console.log("Error al cargar la información de los etiquetas");
            });
            // ------------------------------------------------------------------------------ Getting Empty Model
            $.get(self.getUrlModelEmpty(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.modelEmpty = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar los datos de guardado");
                console.log("Error al cargar la información del modelo vacío");
            });
            // ------------------------------------------------------------------------------ Getting Organization List
            $.get(self.getUrlOrganizations(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_organizations = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar los datos de organizaciones");
                console.log("Error al cargar la información de las organizaciones");
            });
            // ------------------------------------------------------------------------------ Getting Countries List
            $.get(self.getUrlCountries(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_countries = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar los datos de los países");
                console.log("Problema al cargar la información de los países");
            });
            // ------------------------------------------------------------------------------ Getting Projects List
            $.get(self.getUrlProjects(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_projects = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar los datos de los proyectos");
                console.log("Problema al cargar los datos de los proyectos");
            });
            // ------------------------------------------------------------------------------ Getting Types List
            $.get(self.getUrlTypes(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_types = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar los datos de los tipos de beneficiarios");
                console.log("Problema al cargar los datos de los tipos de beneficiarios");
            });
            // ------------------------------------------------------------------------------ Getting Types List
            $.get(self.getUrlEducation(), function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.list_education = data;
            })
                .fail(function () {
                alertify.error("Problema al cargar el catalogo de tipo de educacion");
                console.log("Problema al cargar el catalogo de tipo de educacion");
            });
        },
        removingFromDuplicateListImported: function (ids) {
            var self = this;
            var indexes = [];
            var models = self.modelsNames.filter(function (model, index) {
                if (ids.indexOf(model.contact_id * 1) !== -1) {
                    indexes.push(index);
                    return true;
                }
                return false;
            });
            console.log([models, ids, indexes, self.modelsNames]);
            $.each(models, function (index, model) {
                var i = self.modelsNames.indexOf(model);
                console.log(self.modelsNames.splice(i, 1));
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
            $.post(self.getUrlNameValues(), { ids: self.ids }, function (data, textStatus, jqXHR) {
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
            $.post(self.getUrlFusion(), data, function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                else {
                    self.removingFromDuplicateListImported(self.ids);
                }
                self.fusionResult = data.result;
                self.fusionFlags.result = false;
                self.loading.modal = false;
                self.loading.fusion = false;
                self.modalState = 'finish';
            })
                .fail(function () {
                alertify.error("Problema al fusionar los registros de contacto.");
                self.loading.modal = false;
                self.loading.fusion = false;
            });
        },
        fusionFinish: function () {
            var self = this;
            if (self.modelCurrent) {
                // var index = self.modelsNames.indexOf(self.modelCurrent);
                // self.modelsNames.splice(index, 1);
                self.modelCurrent = null;
            }
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
            self.modelCurrent = model;
            self.loading.modal = true;
            self.name = model.contact_name;
            self.modalState = 'select';
            var url = self.getUrlId(model.contact_id);
            if (!url) {
                self.loading.modal = false;
                console.log("No se logró generar la URL para obtener la información del contacto");
            }
            else {
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
        }
    },
    mounted: function () {
        this.load();
    }
});
