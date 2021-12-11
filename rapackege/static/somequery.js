$(document).ready(function() {
  $('#customer_list').DataTable( {
      select: false
      } );
  var elemt = document.getElementById("customer_list_filter");
  if (elemt != null) {
    elemt.style.display = "none";
  }
//Simple translate with dom need better aproach
} );

