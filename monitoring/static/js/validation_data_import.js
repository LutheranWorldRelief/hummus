$(function () {
    let table = $('#tb_resultados');
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
        let mostrar_boton = ($('.empty-cell-important').length <= 0);
        if (mostrar_boton) {
            $('button[type=submit]').removeClass('d-none');
        } else {
            $('#showBadRecords').removeClass('d-none');

            let filas = table.find('tr');
            filas.each(function () {
                let fila = $(this);
                for (let i = 1; i <= 5; i++) {
                    let celda = fila.find('td').eq(i);
                    if (celda.hasClass('empty-cell-important')) {
                        fila.addClass('tr-missing_data')
                    }
                }
            })
        }


    }

})
