import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let id_usera = document.getElementById("id_getter").value
let detail_usera = JSON.parse(httpGet("/admin_api/detail_usera/" + String(id_usera)))

let tc = new TableCreator(document.getElementById("parent_div"))

detail_usera.forEach(element => {
    tc.make_row([element["display_name"], element["value"]])
});