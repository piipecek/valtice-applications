import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let ucastnici = JSON.parse(httpGet("/org_api/seznam_ucastniku"))
let statistiky = JSON.parse(httpGet("/org_api/statistiky"))

let tc = new TableCreator(document.getElementById("parent_div"), true, true, true)
tc.make_header(["Jméno", "E-mail", "Registrován", "Hlavní třída"])
ucastnici.forEach(element => {
    let jmeno_a = document.createElement("a")
    jmeno_a.href = "/organizator/detail_ucastnika/" + element["id"]
    jmeno_a.innerText = element["full_name"]
    jmeno_a.setAttribute("class", "jmeno-a")
    let trida_span = document.createElement("span")
    if (!element["is_active_participant"]) {
        trida_span.innerText = "Pasivní účast"
    } else if (element["hlavni_trida_id"]) {
        let trida_a = document.createElement("a")
        trida_a.href = "/organizator/detail_tridy/" + element["hlavni_trida_id"]
        trida_a.innerText = element["hlavni_trida"]
        trida_a.classList.add("link")
        trida_span.appendChild(trida_a)
    } else {
        trida_span.innerText = "Zatím nevybrána"
    }
        
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
    tc.make_row([jmeno_a, email_element, element["registrovan"], trida_span])
});

document.getElementById("vsichni").innerText = statistiky.vsichni
document.getElementById("zajemci").innerText = statistiky.zajemci
document.getElementById("zapsani").innerText = statistiky.zapsani
document.getElementById("registrovani").innerText = statistiky.registrovani