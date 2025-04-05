import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let ucty = JSON.parse(httpGet("/org_api/seznam_uctu"))

let tc = new TableCreator(document.getElementById("parent_div"), true, true, true)
tc.make_header(["Jméno", "E-mail", "Datum vytvoření účtu"])
ucty.forEach(element => {
    let jmeno_a = document.createElement("a")
    jmeno_a.href = "/organizator/detail_ucastnika/" + element["id"]
    jmeno_a.innerText = element["full_name"]
    jmeno_a.setAttribute("class", "jmeno-a")
    let trida_span = document.createElement("span")
        
    let email_element
    if (element["email"] == "-") {
        email_element = document.createElement("span")
        email_element.innerText = "-"
    } else {
        let a = document.createElement("a")
        a.href="mailto:" + element["email"]
        a.innerText = element["email"]
        a.classList.add("link")
        email_element = a
    }
    tc.make_row([jmeno_a, email_element, element["datum"]])
});