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
            'contact_type_id',
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
                alertify.error(gettext("Problem loading tags"));
                console.log(gettext("Error loading tag information"));
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
                alertify.error(gettext("Problem loading save data"));
                console.log(gettext("Error loading empty model information"));
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
                alertify.error(gettext("Problem loading organizations data"));
                console.log(gettext("Error loading organizations information"));
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
                alertify.error(gettext("Problem loading country data"));
                console.log(gettext("Problem loading country information"));
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
                alertify.error(gettext("Problem loading project data"));
                console.log(gettext("Problem loading project data"));
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
                alertify.error(gettext("Problem loading data on beneficiary types"));
                console.log(gettext("Problem loading data on beneficiary types"));
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
                alertify.error(gettext("Problem loading the type of education catalog"));
                console.log(gettext("Problem loading the type of education catalog"));
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
                alertify.error(gettext("Problem at "));
                console.log(gettext("Error loading contact information"));
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
                alertify.error(gettext("Problem at "));
                console.log(gettext("Error loading contact information"));
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
                alertify.error(gettext("Problem loading records"));
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
                alertify.error(gettext("Problem merging contact records"));
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
                console.log(gettext("The URL could not be generated to get the contact information"));
            }
            else {
                // @ts-ignore
                $.get(url, function (data, textStatus, jqXHR) {
                    if (textStatus !== 'success')
                        console.log([textStatus, jqXHR]);
                    self.models = data.models;
                })
                    .fail(function () {
                    console.log(gettext("The URL could not be generated to get the contact information"));
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
