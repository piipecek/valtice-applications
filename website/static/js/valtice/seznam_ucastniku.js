import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let ucastnici = JSON.parse(httpGet("/valtice_api/ucastnici"))

let tc = new TableCreator(document.getElementById("parent_div"), true, true, true)
tc.make_header(["Jméno", "E-mail", "Registrován", "Hlavní třída", "Detail"])
ucastnici.forEach(element => {
    let button = document.createElement("button")
    button.classList.add("btn", "btn-success", "btn-narrow")
    button.type = "submit"
    button.innerText = "Detail účastníka"
    button.name="result"
    button.value = element["id"]
    let email_element
    if (element["email"] == "-") {
        email_element = document.createElement("span")
        email_element.innerText = "-"
    } else {
        let a = document.createElement("a")
        a.href="mailto:" + element["email"]
        a.innerText = element["email"]
        email_element = a
    }
    tc.make_row([element["full_name"], email_element, element["registrovan"], element["hlavni_trida_1"], button])
});

document.getElementById("total").innerText = ucastnici.length