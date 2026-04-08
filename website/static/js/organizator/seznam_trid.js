import awaitable_custom_fetch from "../awaitable_custom_fetch.js"
import TableCreator from "../table_creator.js"

let tridy = JSON.parse(await awaitable_custom_fetch("/org_api/seznam_trid"))

let tc = new TableCreator(document.getElementById("parent_div"), true)
tc.make_header(["Název", "Lektor", "Počet účastníků"])

for (let trida of tridy){
    let a = document.createElement("a")
    a.href = "/organizator/detail_tridy/" + trida["id"]
    a.innerText = trida["name"]
    a.classList.add("jmeno-a")

    let links_span = document.createElement("span")
    if (trida["tutor_id"] == null) {
        links_span.innerText = trida["tutor_full_name"]
    } else {
        let lektor_a = document.createElement("a")
        lektor_a.href = "/organizator/detail_ucastnika/" + trida["tutor_id"]
        lektor_a.innerText = trida["tutor_full_name"]
        lektor_a.classList.add("link")
        links_span.appendChild(lektor_a)
    }

    tc.make_row([a, links_span, trida["pocet_ucastniku"]])
}