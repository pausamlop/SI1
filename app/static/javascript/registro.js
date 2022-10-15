$('#formregistro').submit(function() {
    var tarjeta = $('#tarjeta').val();
    var pass1 = $('#pass1').val();
    var pass2 = $('#pass2').val();

    if(tarjeta.length != 16){
        alert('Introduzca los 16 dígitos de la tarjeta seguidos')
    }

    if (pass1!= pass2) {
        alert('Verificación de contraseña errónea');
        return false;
    }

    return true;
});

