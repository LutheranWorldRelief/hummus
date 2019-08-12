function DocumentosService($http, $q, $templateCache) {
    this.Subir = function (url, data) {
        var deferred = $q.defer();
        var formData = new FormData();
        angular.forEach(data, function (value, key) {
            formData.append(key, value);
        });

        opciones = {
            headers: {"Content-type": undefined},
            transformRequest: angular.identity,
            cache: $templateCache
        };

        return $http.post(url, formData, opciones)
                .success(function (res) {
                    deferred.resolve(res);
                })
                .error(function (msg, code) {
                    deferred.reject(msg);
                });

        return deferred.promise;
    }
}

function uploaderModel($parse) {
    return {
        restrict: 'A',
        link: function (scope, iElement, iAttrs) {
            iElement.on("change", function (e) {
                $parse(iAttrs.uploaderModel).assign(scope, iElement[0].files[0]);
            });
        }
    };
}

app.service('DocumentosService', DocumentosService);
app.directive('uploaderModel', uploaderModel);