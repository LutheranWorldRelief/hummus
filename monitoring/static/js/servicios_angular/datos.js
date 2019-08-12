DatosService.$inject = ['$http', '$templateCache'];
function DatosService($http, $templateCache) {
    this.Consultar = function (url, data = {}) {
        return $http({
            method: 'GET',
            url: (url),
            params: data,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            cache: $templateCache
        });
    }
    this.Enviar = function (url, data) {
        return $http({
            method: 'POST',
            url: (url),
            data: $.param(data),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            cache: $templateCache
        });
    }
}
