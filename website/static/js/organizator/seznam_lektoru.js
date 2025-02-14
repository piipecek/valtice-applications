import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"


let lektori = JSON.parse(httpGet("/org_api/seznam_lektoru"))

let tc = new TableCreator(document.getElementById("parent_div"), true)
tc.make_header(["Jméno", "Telefon", "Vyučované třídy"])

for (let lektor of lektori){
    let a = document.createElement("a")
    a.href = "/organizator/detail_ucastnika/" + lektor["id"]
    a.innerText = lektor["full_name"]
    a.classList.add("jmeno-a")
    let links_span = document.createElement("span")
    if (lektor["taught_classes"].length == 0) {
        links_span.innerText = "Žádné"
    } else {
        for (let trida of lektor["taught_classes"]) {
            let trida_a = document.createElement("a")
            trida_a.href = "/organizator/detail_tridy/" + trida["id"]
            trida_a.innerText = trida["short_name"]
            trida_a.classList.add("link")
            links_span.appendChild(trida_a)
            links_span.appendChild(document.createTextNode(", "))
        }
        links_span.lastChild.remove()
    }
    tc.make_row([a, lektor["phone"], links_span])
}