let MergeUrls = {
    data:{
        baseurl:''
    },
    methods:{
        loadBaseUrl: function(elem){
            let self = this;
            // @ts-ignore
            self.baseurl = $(elem).data('baseurl');
        },
        //---------------------------------------------------------------------------------------------- URL FUNCTIONS
        createUrl : function (append) {
            return this.baseurl + append;
        },
        getUrlAll: function () {
            return this.createUrl('opt/api-names')
        },
        getUrlModelLabels: function () {
            return this.createUrl('opt/api-labels')
        },
        getUrlModelEmpty: function () {
            return this.createUrl('opt/api-empty')
        },
        getUrlId: function (id) {
            if(!id)
                return null;
            return this.createUrl('opt/api-contact?id=' + id)
        },
        getUrlName: function (name) {
            if(!name)
                return null;
            return this.createUrl('opt/api-name?name=' + name)
        },
        getUrlNameValues: function () {
            return this.createUrl('opt/api-name-values')
        },
        getUrlFusion: function () {
            return this.createUrl('opt/api-fusion')
        },


        getUrlAllDocs: function () {
            return this.createUrl('opt/api-docs')
        },
        getUrlDoc: function (doc) {
            if(!doc)
                return null;
            return this.createUrl('opt/api-doc?doc=' + doc)
        },
        getUrlDocValues: function () {
            return this.createUrl('opt/api-doc-values')
        },

        getUrlOrganizations: function () {
            return this.createUrl('opt/api-organizations')
        },
        getUrlProjects: function () {
            return this.createUrl('opt/api-projects')
        },
        getUrlCountries: function () {
            return this.createUrl('opt/api-countries')
        },
        getUrlTypes: function () {
            return this.createUrl('opt/api-types')
        },
        getUrlEducation: function () {
            return this.createUrl('opt/api-education')
        },
    }
};