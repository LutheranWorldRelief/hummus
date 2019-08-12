var appVue = new Vue({
    el: "#app",
    mixins: [
        MergeUrls,
    ],
    data: {
        loading: true,
        filter: '',
        projectId: null,
        project: null,
        models: [],
        count: {
            contact: 0,
            projectContact: 0
        },
        labels: {
            contact: {},
            projectContact: {}
        },
        new: {
            contact: null,
            projectContact: null
        },
        modal: {
            loading: false,
            model: {},
            contactIndex: null,
            contact: {},
            errors: {}
        }
    },
    filters: {
        uppercase: function (v) {
            return v.toUpperCase();
        }
    },
    methods: {
        search: function (q) {
            var self = this;
            self.loading = true;
            // ------------------------------------------------------------------------------ Getting Models
            $.get(self.getUrlAll(), { projectId: self.projectId, q: q }, function (data, textStatus, jqXHR) {
                if (textStatus != 'success')
                    console.log([textStatus, jqXHR]);
                self.models = data.models;
                self.labels = data.labels;
                self.count = data.count;
                self.new = data.new;
                self.project = data.project;
            })
                .fail(function () {
                var msg = "Error al cargar la información de los contactos";
                alertify.error(msg);
                console.log(msg);
            })
                .always(function () {
                self.loading = false;
            });
        },
        load: function () {
            var self = this;
            self.projectId = $(self.$el).data('project-id');
            self.loadBaseUrl(self.$el);
            self.search('');
        },
        //---------------------------------------------------------------------------------------------- PREPARING DATA
        modalCancel: function (modalName) {
            var self = this;
            $(modalName).modal('hide');
        },
        modalSave: function (modalName) {
            var self = this;
            self.modal.loading = true;
            self.modal.errors = {};
            var url = self.getUrlSaveProjectContact({
                projectId: self.projectId,
                contactId: self.modal.contact.id
            });
            if (!self.modal.contact) {
                alertify.error("No se consiguió cargar el modelo de Beneficiario");
                return;
            }
            if (self.modal.contactIndex < 0) {
                alertify.error("No se consiguió cargar el índice del Beneficiario");
                return;
            }
            if (!url) {
                self.modal.loading = false;
                alertify.error("No se logró generar la URL para obtener la información del contacto");
            }
            else {
                var dataPost = {
                    ProjectContact: self.modal.model
                };
                $.post(url, dataPost, function (data, textStatus, jqXHR) {
                    if (textStatus !== 'success')
                        console.log([data, textStatus, jqXHR]);
                    var contactIndex = self.modal.contactIndex;
                    self.models[contactIndex].projectContactOne = self.modal.model;
                    $(modalName).modal('hide');
                    alertify.success('Los datos se han guardado correctamente');
                })
                    .fail(function (jqXHR, textStatus, errorThrown) {
                    alertify.error('Se ha producido un error. Favor revisar los datos introducidos.');
                    if (errorThrown == 'error_registro_dato') {
                        self.modal.errors = jqXHR.responseJSON.projectContact.errors;
                    }
                })
                    .always(function () {
                    self.modal.loading = false;
                    self.modalLoadDatepicker(null);
                });
            }
        },
        modalLoadDatepicker: function (event) {
            var self = this;
            var jq = $('.datepicker');
            if (jq.data('kvDatepicker'))
                jq.kvDatepicker('destroy');
            jq.kvDatepicker({
                format: "yyyy-mm-dd",
                language: "es"
            });
            $('#date_end').kvDatepicker('setDate', self.modal.model.date_end_project);
            $('#date_entry').kvDatepicker('setDate', self.modal.model.date_entry_project);
            $('#date_end').on('changeDate', function (event) {
                self.modal.model.date_end_project = $('#date_end').val();
            });
            $('#date_entry').on('changeDate', function (event) {
                self.modal.model.date_entry_project = $('#date_entry').val();
            });
        },
        modalEdit: function (contact, index) {
            var self = this;
            if (contact && (index >= 0)) {
                self.modal.contact = contact;
                self.modal.contactIndex = index;
                self.modal.errors = {};
                if (!contact.projectContactOne)
                    self.modal.model = Object.assign({}, self.new.projectContact);
                else
                    self.modal.model = Object.assign({}, contact.projectContactOne);
            }
            return false;
        }
    },
    mounted: function () {
        this.load();
    }
});
