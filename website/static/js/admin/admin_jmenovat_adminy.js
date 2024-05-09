import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let uzivatele_pro_udeleni_roli = JSON.parse(httpGet("/admin_api/uzivatele_pro_udeleni_roli"))

let tc1 = new TableCreator(document.getElementById("parent_div_1"))
tc1.make_header(["#", "E-mail", "Vybrat"])
let tc2 = new TableCreator(document.getElementById("parent_div_2"))
tc2.make_header(["#", "E-mail", "Vybrat"])

uzivatele_pro_udeleni_roli.users.forEach(element => {

    let button = document.createElement("button")
    button.classList.add("btn", "btn-success")
    button.innerHTML = "Vybrat"
    button.name="result"
    button.value = element["id"]

    tc1.make_row([element["id"], element["email"], button])
});

uzivatele_pro_udeleni_roli.admins.forEach(element => {

    let button = document.createElement("button")
    button.classList.add("btn", "btn-success")
    button.innerHTML = "Vybrat"
    button.name="result"
    button.value = element["id"]
    tc2.make_row([element["id"], element["email"], button])
});