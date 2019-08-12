'use strict';
var app = angular.module("App", ['angularUtils.directives.dirPagination']);
app.service('DatosService', DatosService);
//app.constant('UrlsAcciones', UrlsAcciones);
function ValoresCtrl($scope, $http, $q, $templateCache, DatosService) {
        $scope.tamanioPagina = 10;
        $scope.nuevo = function () {
            $scope.tituloModal = "Nuevo Registro";
            $scope.setNuevo();
            $('#formularioModal').modal('show');
        }

        $scope.editar = function (obj) {
            $scope.tituloModal = "Registro [" + obj.nombre + "]";
            $scope.formulario = {};
            angular.copy(obj, $scope.formulario);
            $scope.setActualizar();
            $('#formularioModal').modal('show');
        }

        $scope.eliminar = function (obj) {

            var url = $scope.acciones.eliminar;
            var data = {};

            if (obj.hasOwnProperty('id'))
                data.id = obj.id;
            else {
                alertify.error('No se posible identificar el registro apropiadamente');
                return;
            }

            alertify.confirm('¿Esta seguro que desea eliminar este registro?', function (e) {
                if (e) {
                    DatosService
                            .Enviar(url, data)
                            .then(function (respuesta) {
                                if (respuesta.estado === 'ok') {
                                    alertify.success('Registro eliminado correctamente');
                                    $scope.obtenerValores();
                                } else {
                                    alertify.error('No se logró eliminar el registro especificado');
                                }
                            })
                            .catch(function (mensaje, codigo) {
                                alertify.error('Error al modificar ' + mensaje + ' Código de Error ' + codigo);
                            });
                }
                else {
                    alertify.error('Se ha cancelado');
                }
            });
        }

        $scope.cerrarModal = function () {
            $('#formularioModal').modal('hide');
            $scope.formulario = {};
            $scope.search = '';
            $scope.formularioVisible = false;
            $scope.obtenerValores();
            $scope.setNuevo();
        }

        $scope.guardar = function (obj) {

            var url = $scope.acciones.nuevo;
            var data = {data: obj};

            if (obj.hasOwnProperty('id')) {
                url = $scope.acciones.actualizar;
                data.id = obj.id;
            }

            DatosService
                    .Enviar(url, data)
                    .then(function (respuesta) {
                        if (respuesta.estado === 'ok') {
                            $('#formularioModal').modal('hide');
                            $scope.formulario = {};
                            $scope.obtenerValores();
                            alertify.success('Registro guardado correctamente');
                        } else {
                            $scope.formulario._errors = respuesta.errores;
                            alertify.error('Registro no guardado, verifique');
                        }
                    })
                    .catch(function (mensaje, codigo) {
                        alertify.error('Error al modificar ' + mensaje + ' Código de Error ' + codigo);
                    });

        }

        $scope.obtenerValores = function () {
            var url = $scope.acciones.registros;
            $scope.valores = [];

            DatosService
                    .Consultar(url)
                    .then(function (respuesta) {
                        $scope.valores = respuesta;
                    })
                    .catch(function (mensaje, codigo) {
                        alertify.error('Error al modificar ' + mensaje + ' Código de Error ' + codigo);
                    });
        }

        $scope.ordenar = function (campo) {
            $scope.sortKey = campo;   //set the sortKey to the param passed
            $scope.reverse = !$scope.reverse; //if true make it false and vice versa
        }

        $scope.estiloError = function (cadena) {

            if (cadena)
                return "border-color:#a94442;";
            else
                return '';
        }

        $scope.setNuevo = function () {
            $scope.nuevoRegistro = true;
            $scope.etiqueta = " Agregar";
            $scope.clase = 'btn-success';
            $scope.icono = 'plus';
        };

        $scope.setActualizar = function () {
            $scope.nuevoRegistro = false;
            $scope.etiqueta = ' Modificar';
            $scope.clase = 'btn-primary';
            $scope.icono = 'pencil';
        };

        $scope.$watch('acciones', function () {
            $scope.obtenerValores();
        });

    }
app.controller('ValoresCtrl', ValoresCtrl);