$(function () {
    var tableParticipants = $('#tableParticipants');
    $('[data-toggle="tooltip"]').tooltip();
    validationData();

    $('body')
        .on('click', '#showBadRecords', function () {

            let label = {
                text1: gettext('Show only records with missing data'),
                text2: gettext('Show all records'),
            };

            if ($(this).hasClass('showdata')) {
                $(this).text(label.text2);
                $(this).removeClass('showdata');
                table.find('tr:not(.tr-missing_data)').fadeOut('slow');
            } else {
                $(this).text(label.text1);
                $(this).addClass('showdata');
                table.find('tr:not(.tr-missing_data)').fadeIn('slow');
            }
        });


    function validationData() {
        let array_index = getColumnAddClass();
        let mostrar_boton = ($('.empty-cell-important').length <= 0);
        if (mostrar_boton) {
            $('button[type=submit]').removeClass('d-none');
        } else {
            $('#showBadRecords').removeClass('d-none');

            let filas = tableParticipants.find('#resultados tr');
            filas.each(function () {
                let fila = $(this);
                for (let index of array_index) {
                    let celda = fila.find('td').eq(index);
                    if (celda.hasClass('empty-cell-important')) {
                        fila.addClass('tr-missing_data')
                    }
                }
            })
        }
    }

    function getColumnAddClass() {
        let array_index = [];
        tableParticipants.find('thead tr th').each(function (index) {
            let cell = $(this);
            if (columns_required.includes(cell.text())) {
                array_index.push(index)
            }
        });
        if (array_index.length > 0) {

            let filas = tableParticipants.find('#resultados tr');
            filas.each(function () {
                let fila = $(this);
                for (let index of array_index) {
                    let celda = fila.find('td').eq(index);
                    if (celda.text().length <= 0) {
                        celda.addClass('empty-cell-important');
                        break;
                    }
                }
            })
        }
        return array_index;
    }

});
