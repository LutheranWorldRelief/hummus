function AttendanceModel() {
    var obj = {
        contact_id: "",
        fullname: "",
        document: "",
        org_id: "",
        org_name: "",
        sex: "",
        country_id: "",
        community: "",
        type_id: "",
        type_tags: "",
        phone_personal: "",
        errors: {},
        loading_contact: false,
        loading_org: false

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

Vue.component('autocomplete', {
    template: '<input v-model="value" type="text" @keydown="keydown($event)" @keyup="keyup($event)" />',
    props: ['url', 'value'],
    methods: {
        keydown: function (event) {
            event.data = this.value;
            this.$emit('keydown', event);
        },
        keyup: function (event) {
            event.data = this.value;
            this.$emit('keyup', event);
        }
    },
    mounted: function () {
        var self = this;
        var input = $(self.$el);
        input.typeahead({
            source: function (query, process) {
                return $.get(self.url + query, function (data) {
                    return process(data);
                });
            },
            afterSelect: function (value) {
                self.$emit('select', value);
            }
        });
    }
});

var newForm = new Vue({
    el: '#event-form',
    data: {
        app: {},
        model: new AttendanceModel(),
        attendances: [],
        errors: {}
    },
    methods: {
        newAttendance: function () {
            this.attendances.push(Vue.util.extend({}, this.model));
        },
        removeAttendance: function (model, index) {
            this.attendances.splice(index, 1);
        },
        afterSelectContact: function (event, m, index) {
            console.log(event);
            m.contact_id = event.id;
            m.document = event.document;
            m.sex = event.sex;
            m.fullname = event.name;
            m.org_id = event.org_id;
            m.org_name = event.org_name;
            m.country_id = event.country_id;
            m.community = event.community;
            m.type_id = event.type_id;
            m.phone_personal = event.phone_personal;
        },
        afterSelectDoc: function (event, m, index) {
            event = event.model;
            m.contact_id = event.id;
            m.document = event.document;
            m.sex = event.sex;
            m.fullname = event.name;
            m.org_id = event.org_id;
            m.org_name = event.org_name;
            m.country_id = event.country_id;
            m.community = event.community;
            m.type_id = event.type_id;
            m.phone_personal = event.phone_personal;
        },
        afterSelectOrg: function (event, m, index) {
            m.org_id = event.id;
            m.org_name = event.name;
        },
        orgKeyUp: function (event, model) {
            model.org_name = event.data;

        },
        docKeyUp: function (event, model) {
            model.document = event.data;
        },
        nameKeyUp: function (event, model) {
            model.fullname = event.data;
        },
        orgKeyDown: function (event, model) {
            var id = model.org_id;
            model.org_id = "";
            if (event.keyCode == 8 || event.keyCode == 46 || event.keyCode == 35 || event.keyCode == 36)
                return;
            model.org_id = id;
            if (event.keyCode == 9)
                return;
            if (event.keyCode == 13) {
                event.preventDefault();
                return false;
            }
        },
        docKeyDown: function (event, model) {
            // KepPress Alfanumeric
            if ((event.keyCode >= 65 && event.keyCode <= 90) || (event.keyCode >= 96 && event.keyCode <= 105))
                return;
            if ((event.keyCode >= 48 && event.keyCode <= 57) && !event.shiftKey)
                return;
            if (event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 46 || event.keyCode == 35 || event.keyCode == 36)
                return;
            event.preventDefault();
            return false;
        },
        nameKeyDown: function (event, model) {
            var id = model.contact_id;
            model.contact_id = "";
            // KepPress Alfanumeric
            if ((event.keyCode >= 65 && event.keyCode <= 90) || (event.keyCode >= 96 && event.keyCode <= 105))
                return;
            // KepPress Numbers
            if ((event.keyCode >= 48 && event.keyCode <= 57) && !event.shiftKey)
                return;
            // Pressing 8.Backspace, 20.capslock, 46.Delete
            if (event.keyCode == 8 || event.keyCode == 20 || event.keyCode == 46)
                return;
            model.contact_id = id;
            if (event.keyCode == 35 || event.keyCode == 36) //35.Inicio, 36.Fin,
                return;
            if (event.keyCode == 9) //Tab key
                return;
            if (event.keyCode == 13) // Enter Key
            {
                event.preventDefault();
                return false;
            }
        },
    },
    computed: {
        success: function (val) {
            return val ? 'link_success' : '';
        }
    },
    mounted: function () {
        var self = this;
        var options = JSON.parse($('#vue-options').text());
        for (attr in options) {
            self[attr] = options[attr];
        }
    }
});