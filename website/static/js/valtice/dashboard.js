import httpGet from "../http_get.js"
let seznam_trid = JSON.parse(httpGet("/valtice_api/tridy_long_names_ids"))

var selectElement = document.getElementById('select_tridy');

for (var i = 0; i < seznam_trid.length; i++) {
    var option = document.createElement("option"); // Create a new option element
    option.value = seznam_trid[i].id; // Set the value attribute to the id
    option.text = seznam_trid[i].short_name; // Set the text content to the short_name
    selectElement.appendChild(option); // Append the option to the select element
}