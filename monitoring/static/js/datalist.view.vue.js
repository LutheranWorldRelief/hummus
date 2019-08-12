function DataListModel() {
    var obj = {
        description: null,
        value: null,
        notes: null,
        order: null
    };

    obj.clear = function () {
        for (attr in obj) {
            if (!(obj[attr] instanceof Function)) {
                obj[attr] = null;
            }
        }
    }

    obj.load = function (values) {
        obj.clear();
        for (attr in values) {
            obj[attr] = values[attr];
        }
    }

    return obj;
};

var newForm = new Vue({
    el: '#detail-modal',
    data: {
        model: new DataListModel(),
        errors: {}
    },
    methods: {
        saveNewDetail: function (e) {

            var self = this;
            var form = $('#detail-form');

            form.data('yiiActiveForm').submitting = true;
            form.yiiActiveForm('validate');
            form.on('afterValidate', function (event, message, errorAttributes) {
                form.off('afterValidate');
                if (form.find('.has-error').length) {
                    alertify.error('El formulario contiene errores');
                    return;
                }

                $.post(form.attr('action'), {DataList: self.model})
                    .done(function (response) {
                        $.pjax.reload({container: '#grid-details-pjax'});
                        if (response.success) {
                            alertify.success('Registro Agregado!');
                            self.errors = {};
                            // self.model.clear();
                        }
                        else {
                            alertify.error('Error al Guardar');
                            self.errors = response.errors;
                        }
                    })
                    .fail(function (response) {
                        console.log(response);
                    });

            });
        }
    }
});

var editForm = new Vue({
    el: '#detail-modal-edit',
    data: {
        model: new DataListModel(),
        errors: {}
    },
    methods: {
        saveDetail: function (e) {
            var self = this;
            var form = $('#detail-form-edit');

            form.data('yiiActiveForm').submitting = true;
            form.yiiActiveForm('validate');
            form.on('afterValidate', function (event, message, errorAttributes) {

                event.preventDefault();

                form.off('afterValidate');
                if (form.find('.has-error').length) {
                    alertify.error('El formulario contiene errores');
                    return;
                }

                var url = form.attr('action') + '?id=' + self.model.id;
                var data = Vue.util.extend({}, self.model);
                $.post(url, {DataList: data})
                    .done(function (response) {
                        self.model = data;
                        $.pjax.reload({container: '#grid-details-pjax'});
                        if (response.success) {
                            alertify.success('Registro Agregado!');
                            self.errors = {};
                        }
                        else {
                            alertify.error('Error al Guardar');
                            self.errors = response.errors;
                        }
                    })
                    .fail(function (response) {
                        console.log(response);
                    });
            });
        }
    }
});

function loadDetail(event, sender) {
    $.get(sender.attr('data-url'))
        .done(function (response) {
            editForm.model.load(response);
        });
}