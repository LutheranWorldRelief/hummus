var MergeUrls = {
    data: {
        baseurl: ''
    },
    methods: {
        loadBaseUrl: function (elem) {
            var self = this;
            // @ts-ignore
            self.baseurl = $(elem).data('baseurl');
        },
        //---------------------------------------------------------------------------------------------- URL FUNCTIONS
        createUrl: function (append) {
            return this.baseurl + append;
        },
        getUrlAll: function () {
            return this.createUrl('api/names/');
        },
        getUrlAllFuzzy: function () {
            return this.createUrl('api/names-fuzzy/');
        },
        getUrlModelLabels: function () {
            return this.createUrl('api/labels/');
        },
        getUrlModelEmpty: function () {
            return this.createUrl('api/empty/');
        },
        getUrlId: function (id) {
            if (!id)
                return null;
            return this.createUrl('api/contact/' + id + '/');
        },
        getUrlIds: function (id1, id2) {
            if (!id1 || !id2)
                return null;
            return this.createUrl('api/ids/' + id1 + '/' + id2 + '/');
        },
        getUrlName: function (name) {
            if (!name)
                return null;
            return this.createUrl('api/name/' + name + '/');
        },
        getUrlNameValues: function () {
            return this.createUrl('api/name-values/');
        },
        getUrlFusion: function () {
            return this.createUrl('api/fusion/');
        },
        getUrlAllDocs: function () {
            return this.createUrl('api/docs/');
        },
        getUrlDoc: function (doc) {
            if (!doc)
                return null;
            return this.createUrl('api/doc/' + doc + '/');
        },
        getUrlDocValues: function () {
            return this.createUrl('api/doc-values/');
        },
        getUrlOrganizations: function () {
            return this.createUrl('api/organizations/');
        },
        getUrlProjects: function () {
            return this.createUrl('api/projects/');
        },
        getUrlCountries: function () {
            return this.createUrl('api/countries/');
        },
        getUrlTypes: function () {
            return this.createUrl('api/types/');
        },
        getUrlEducation: function () {
            return this.createUrl('api/education/');
        },
    }
};
