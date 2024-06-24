import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"


let tridy = JSON.parse(httpGet("/valtice_api/tridy"))

let tc = new TableCreator(document.getElementById("parent_div"))
tc.make_header(["Název", "Detail"])

for (let trida of tridy){
    let detail_button = document.createElement("button")
    detail_button.innerText = "Detail"
    detail_button.classList.add("btn", "btn-primary")
    detail_button.name = "trida"
    detail_button.value = trida["id"]
    tc.make_row([trida["short_name"], detail_button])
}