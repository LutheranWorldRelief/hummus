app.directive('wbSelect2', function () {
    return {
        restrict: 'A',
        link: function (scope, element, iAttrs) {
            var opciones = {}
            switch (iAttrs['wbSelect2']) {
                case 'no-clear':
                    opciones = {};
                    break;
                default:
                    opciones = {allowClear: true}
            }
            scope.$watch(iAttrs['ngModel'], function (newValue, oldValue) {
                element.select2(opciones).select('val', newValue);
            });
            element.select2(opciones);
        }
    };
});
app.directive('iCheck', function ($timeout, $parse) {
    return {
        require: 'ngModel',
        link: function ($scope, element, $attrs, ngModel) {
            return $timeout(function () {
                var value = $attrs.value;
                var $element = $(element);

                // Instantiate the iCheck control.                            
                $element.iCheck({
                    checkboxClass: 'icheckbox_flat-green',
                    radioClass: 'iradio_square-green',
                    increaseArea: '5%'
                });

                // If the model changes, update the iCheck control.
                $scope.$watch($attrs.ngModel, function (newValue) {
                    $element.iCheck('update');
                });

                // If the iCheck control changes, update the model.
                $element.on('ifChanged', function (event) {
                    if ($element.attr('type') === 'radio' && $attrs.ngModel) {
                        $scope.$apply(function () {
                            ngModel.$setViewValue(value);
                        });
                    }
                    if ($element.attr('type') === 'checkbox' && $attrs.ngModel) {
                        $scope.$apply(function () {
                            ngModel.$setViewValue(event.target.checked);
                        });
                    }
                });

            });
        }
    };
});
app.filter("capitalize", function () {
    return function (text) {
        if (text != null)
            return text.substring(0, 1).toUpperCase() + text.substring(1);
    };
});

app.directive('ngNumeric', [function () {
        return {
            restrict: 'A',
            link: function (scope, iElement, iAttrs) {
                switch (iAttrs['ngNumeric']) {
                    case 'entero':
                        iElement.autoNumeric('init', {
                            mDec: 0,
                            vMin: 0
                        });
                        break;
                    default:
                        iElement.autoNumeric();
                }
            }
        };
    }]);

app.directive('ngDate', [function () {
        return {
            restrict: 'A',
            link: function (scope, iElement, iAttrs) {
                iElement.datepicker({
                    closeText: 'Cerrar',
                    prevText: '<Ant',
                    nextText: 'Sig>',
                    currentText: 'Hoy',
                    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                    monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                    dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
                    dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Juv', 'Vie', 'Sáb'],
                    dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
                    weekHeader: 'Sm',
                    dateFormat: 'yy-mm-dd', firstDay: 1,
                    isRTL: false,
                    showMonthAfterYear: false,
                    yearSuffix: '',
                    showOtherMonths: true,
                    selectOtherMonths: true,
                    changeMonth: true,
                    changeYear: true,
                    showButtonPanel: true,
                    yearRange: '-120:+15'
                });
            }
        };
    }]);