function busqueda() {
  var input, filter, table, tr, td, cell, i, j;
  filter = document.getElementById("barra").value.toUpperCase();
  table = document.getElementById("tabla");
  tr = table.getElementsByTagName("tr");
  for (i = 1; i < tr.length; i++) {
    tr[i].style.display = "none";
    const tdArray = tr[i].getElementsByTagName("td");
    for (var j = 0; j < tdArray.length; j++) {
      const cellValue = tdArray[j];
      if (cellValue && cellValue.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
        break;
      }
    }
  }
}