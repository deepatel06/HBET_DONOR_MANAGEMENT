
  function readTableData(){
  
      //gets table
      var eTable = document.getElementById('dtable');
  
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
          alert("Changes Saved Successfully")
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
function bid_data(data){
// Extract value from table header. 
    // ('Book ID', 'Book Name', 'Category' and 'Price')
    let col = ["ID","First Name","Last Name","Full Name","Email","Date Of Birth(YYYY-MM-DD)","Date Of Marriage","Spouse Name","Address 1","Address 2","Date Of Registration","City","State","Pincode","Mobile Number 1","Mobile Number 2","Aadhar Card Number","Pan Card Number","Password"];

    let col_db = ["id","first_name","last_name","full_name","email","dob","dom","spouse_name","address1","address2","dor","city","state","pin_code","mobile1","mobile2","aadhar_card","pan_card","password"];



    console.log(col)
    // Create table.
    const table = document.createElement("table");
    table.id = "dtable"

    // Create table header row using the extracted headers above.
    let tr = table.insertRow(-1);                   // table row.
    li=[]
    for (let i = 0; i < col.length; i++) {
      let th = document.createElement("th");      // table header.
      th.innerHTML = col[i];
      tr.appendChild(th);
    }

    // add json data to the table as rows.
    for (let i = 0; i < data.length; i++) {

      tr = table.insertRow(-1);
      tr.id = "tr" +i
      ii = "tr" +i
      li.push(ii)

      for (let j = 0; j < col.length; j++) {
        let tabCell = tr.insertCell(-1);
      console.log( data[i][col_db[j]])
        tabCell.innerHTML = data[i][col_db[j]];
       
       
      }
    }

    // Now, add the newly created table with json data, to a container.
    const divShowData = document.getElementById('dataTable');
    divShowData.innerHTML = "";
    divShowData.appendChild(table);
    console.log("in bind")

    console.log(li)
    for (let i = 0; i < li.length; i++) {
      
       
        document.getElementById(li[i]).contentEditable = "true";
        
      
    }
    
   
  }
  bid_data(data)
  console.log(data,"dataa")   
