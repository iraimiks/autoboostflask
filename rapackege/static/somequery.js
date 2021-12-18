$(document).ready(function() {
  $('#customer_list').DataTable( {
      select: false
      } );
  var elemt = document.getElementById("customer_list_filter");
  if (elemt != null) {
    elemt.style.display = "none";
  }
} );

$(document).ready(function() {
  $('#all_orders').DataTable( {
      select: false
      } );
  var elemt = document.getElementById("all_orders_filter");
  if (elemt != null) {
    elemt.style.display = "none";
  }
} );