'use strict';
var app = angular.module("App", ['angularUtils.directives.dirPagination',  'ngSanitize']);
app.service('DatosService', DatosService);
app.constant('UrlsAcciones', UrlsAcciones);
app.controller('AppCtrl', CRUD);
