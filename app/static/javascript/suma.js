// function suma(movies){
//     var total=0
//     console.log(arguments[0]);
//     // for (item in movies){
//     //     total =+ item.precio;
//     // }
//     $(document).find(".total").html(total.toFixed(2))
//     return(total);
// }

$(document).ready(function()
{
  
  var total_col1 = 0;

  //Recorro todos los tr ubicados en el tbody
  $('#econtent-table tbody').find('tr').each(function (i, el) {
             
        //Voy incrementando las variables segun la fila ( .eq(0) representa la fila 1 )     
        total_col1 += parseFloat($(this).find('td').eq(3).text());
       
                
    });
    //Muestro el resultado en el th correspondiente a la columna
    $('#ejemplo tfoot tr th').eq(3).text("Total " + total_col1);
    

});
