function personas_conectadas(){
    $.ajax({url: "/usu_conectados",method: "GET", 
            success: function(result){$('#conectados').html(result)}});
}

$(document).ready(function() {
    setInterval(personas_conectadas, 3000)
});


