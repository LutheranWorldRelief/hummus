var MergeUrls = {
    data: {
        baseurl: ''
    },
    methods: {
        loadBaseUrl: function (elem) {
            var self = this;
            self.baseurl = $(elem).data('baseurl');
        },
        //---------------------------------------------------------------------------------------------- URL FUNCTIONS
        createUrl: function (append, params) {
            var url = this.baseurl + append;
            if (params)
                url += '?' + $.param(params);
            return url;
        },
        getUrlAll: function (params) {
            return this.createUrl('project/api-contacts', params);
        },
        getUrlSaveProjectContact: function (params) {
            return this.createUrl('project/api-contact', params);
        },
    }
};
