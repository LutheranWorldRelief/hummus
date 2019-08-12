function CRUD($scope, UrlsAcciones, DatosService, $sce, $timeout) {

    $scope.UrlNuevo = UrlsAcciones.nuevo;
    $scope.UrlActualizar = UrlsAcciones.actualizar;
    $scope.UrlEliminar = UrlsAcciones.eliminar;
    $scope.UrlDatosGrid = UrlsAcciones.registros;
    $scope.Select2 = UrlsAcciones.select2;
    $scope.nuevoRegistro = true;
    $scope.formulario = {};
    $scope.tamanioPagina = 10;

    $scope.cargarRegistrosGrid = function () {
        DatosService
                .Consultar($scope.UrlDatosGrid)
                .then(function (result) {
                    $scope.registros = result.data;
                })
                .catch(function (mensaje, codigo) {
                    alertify.error('Error al cargar ' + mensaje + ' Código de Error ' + codigo);
                });
    };

    $scope.nuevo = function () {
        DatosService
                .Enviar($scope.UrlNuevo, $scope.formulario)
                .then(function (result) {
                    Validaciones(result.data, true);
                })
                .catch(function (mensaje, codigo) {
                    alertify.error('Error al crear ' + mensaje + ' Código de Error ' + codigo);
                });

    };

    $scope.actualizar = function () {
        DatosService
                .Enviar($scope.UrlActualizar, $scope.formulario)
                .then(function (result) {
                    Validaciones(result.data, false);
                })
                .catch(function (mensaje, codigo) {
                    alertify.error('Error al modificar ' + mensaje + ' Código de Error ' + codigo);
                });

    };

    function Validaciones(data, nuevo) {
        if (data.estado === 'ok') {
            $scope.limpiarFormulario();
            if (nuevo) {
                alertify.success('Registro agregado correctamente');
            } else
                alertify.success('Registro actualizado correctamente');

        } else {
            $scope.formulario._errors = data.errores;
            alertify.error('Registro no guardado, verifique');
        }


    }

    $scope.eliminar = function (id) {

        alertify.confirm('Esta seguro que desea eliminar?', function (e) {
            if (e) {
                DatosService
                        .Enviar($scope.UrlEliminar, id)
                        .then(function (data) {
                            $scope.limpiarFormulario();
                            alertify.success('Registro eliminado correctamente');
                        })
                        .catch(function (mensaje, codigo) {
                            alertify.error('Error al eliminar ' + mensaje + ' Código de Error ' + codigo);
                        });

            } else {
                alertify.error('Se ha cancelado');
            }
        })

    };

    $scope.Ordenar = function (campo) {
        $scope.sortKey = campo;   //set the sortKey to the param passed
        $scope.reverse = !$scope.reverse; //if true make it false and vice versa
    };

    $scope.enviar = function () {
        $scope.nuevoRegistro ? $scope.nuevo() : $scope.actualizar();
    };

    $scope.setSelect2 = function () {
        $timeout(function () {
            $('select.select2').select2({allowClear: true});
        }, 250);
    }

    $scope.mostrarCrear = function () {
        $('#formularioModal').modal('show');
        $scope.formularioVisible = true;
        if ($scope.Select2)
            $scope.setSelect2();
    };

    $scope.mostrarEditar = function (registro) {
        $('#formularioModal').modal('show');
        $scope.formularioVisible = true;
        $scope.formulario = registro;
        $scope.setActualizar();
        if ($scope.Select2)
            $scope.setSelect2();
    };

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

    $scope.limpiarFormulario = function () {
        $('#formularioModal').modal('hide');
        $scope.formulario = {};
        $scope.search = '';
        $scope.formularioVisible = false;
        $scope.cargarRegistrosGrid();
        $timeout(function () {
            $scope.setNuevo();
        }, 550);

    };

    $scope.EstiloError = function (cadena) {
        if (cadena)
            return "border-color:#a94442;";
        else
            return '';
    };

    $scope.limpiarFormulario();

    $scope.Html = function ($print) {
        return $sce.trustAsHtml($print);
    };
    $scope.HtmlLink = function ($print, $link, id) {
        return  $scope.Html('<a href="' + $link + id + '" title="Detalle">' + $print + '</a>');
    };
}
