function compute()
{   //getting input value into the function
    var p = document.getElementById("principal").value;
    var r = document.getElementById("rate").value;
    var y = document.getElementById("years").value;
  
// Validation of positive number for "principal" input
    if (p <= 0){window.alert("Enter a positive number")
document.getElementById("principal").focus();}
   else {         
//calcuation of interest
    var interest = p * r * y / 100;

//adding the current year with the year input
    var yearNow = new Date().getFullYear();
    var yearsFromNow = (+yearNow) + (+y);
//display result from calculation
var result = document.getElementById("result");
    result.innerHTML = 
        '<div>' +
            'If you deposit <span class="number" id="principalResult\">' + p + '</span>,<br/>' +
            'at an interest rate of <span class="number" id="rateResult">' + r + '%</span>.<br/>' +
            'You will receive an amount of <span class="number" id="interestResult">' + interest + '</span>,<br/>' +
            'in the year <span class="number" id="futureYearResult">' + yearsFromNow + '</span>.<br/>' +
        '</div>'
}  
}

function slider()
{ //display the value from slider
    var sv = document.getElementById("rate").value;
document.getElementById("slider_value").innerHTML = sv + "%";}