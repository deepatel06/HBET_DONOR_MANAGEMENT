$(document).ready(function() {
  $('#dataTable').DataTable({

      scrollY: '500px',
      scrollX: '11px',
      paging: false,


    });
});
function readTableData(){

    //gets table
    var eTable = document.getElementById('dataTable');

    //gets rows of table
    var rowLength = eTable.rows.length;

    var totalEmp = [];
    var headers = [];

    //loops through rows
    for (i = 0; i < rowLength; i++){

        //gets cells of current row
        var oCells = eTable.rows.item(i).cells;

        //gets count of cells of current row
        var cellLength = oCells.length;

        var rowData = {};

        //loops through each cell in current row
        for(var j = 0; j < cellLength; j++){
            if(i==0){
                //reading the table headers
                /* get your cell info here */
                var cellVal = oCells.item(j).innerText;
                headers.push(cellVal);
            }else{
                //reading the table data
                var cellVal = oCells.item(j).innerText;
                var headerName = headers[j];
                rowData[headerName] = cellVal;
            }

        }
        //skip adding first row (header row) to total record
        if(i!=0){
            totalEmp.push(rowData);
        }
    }
   data = JSON.stringify(totalEmp);
   console.log(JSON.stringify(totalEmp));
   console.log(totalEmp);
   $.ajax({
    type: "POST",
    url: '/updatedonordetailsdb',
    data: {
        "data": data,
    },
    dataType: "json",
    success: function (data) {
        // any process in data
        alert("Changes are saved successfully")
    },
    failure: function () {
        alert("failure");
    }
});
}

 document.getElementById("cancelBtn").addEventListener("click", function() {
    var confirmCancel = confirm("Are you sure you want to cancel changes?");
    console.log(confirmCancel)
    if (confirmCancel) {
      // Perform cancellation logic or page navigation
      // For example: location.href = 'cancel.html';
      location.reload();
    } else {
      // Continue with other actions or stay on the same page
    }
  });


function redirect(){
window.location.href = "/donordetails";

}

