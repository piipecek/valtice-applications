import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let uzivatele_pro_udeleni_roli = JSON.parse(httpGet("/org_api/uzivatele_pro_udeleni_roli"))

let tc1 = new TableCreator(document.getElementById("parent_div_stavajici"))
tc1.make_header(["Jméno", "E-mail", "Role", "Změnit role", "Detail"])

let tc2 = new TableCreator(document.getElementById("parent_div_novi"))
tc2.make_header(["Jméno", "E-mail", "Změnit role", "Účet"])

uzivatele_pro_udeleni_roli.forEach(element => {

    let a = document.createElement("a")
    a.href = "/organizator/udelit_role/" + String(element["id"])

    let role_button = document.createElement("button")
    role_button.classList.add("custom_button")
    role_button.innerText = "Role"
    role_button.type = "button"
    a.appendChild(role_button)

    let ucet_a = document.createElement("a")
    ucet_a.href = "/organizator/detail_ucastnika/" + String(element["id"])

    let ucet_button = document.createElement("button")
    ucet_button.classList.add("custom_button")
    ucet_button.innerText = "Účet"
    ucet_button.type = "button"
    ucet_a.appendChild(ucet_button)


    if (element["role"] == "") {
        tc2.make_row([element["name"], element["email"], a, ucet_a])
    } else {
        tc1.make_row([element["name"], element["email"], element["role"], a, ucet_a])
    }
});