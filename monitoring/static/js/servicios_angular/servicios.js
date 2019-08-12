function errores() {
    this.EstiloError = function (error) {
        if (error)
            return "{'border-color':'#a94442'}";
        else
            return '';
    };
}
function matematica() {
    this.suma = function (objetos, campo) {
        var sum = 0;
        angular.forEach(objetos, function (obj) {
            sum += StrToFloat(obj[campo]);
        });
        return sum;
    };
    this.sumaText = function (objetos, campo) {
        return addCommas(this.suma(objetos, campo));
    };
}