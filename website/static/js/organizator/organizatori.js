import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let uzivatele_pro_udeleni_roli = JSON.parse(httpGet("/admin_api/uzivatele_pro_udeleni_roli"))

let tc = new TableCreator(document.getElementById("parent_div"))
tc.make_header(["#", "E-mail", "Role", "Detail"])

uzivatele_pro_udeleni_roli.forEach(element => {

    let a = document.createElement("a")
    a.href = "/organizator/detail_usera/" + String(element["id"])

    let button = document.createElement("button")
    button.classList.add("custom_button")
    button.innerHTML = "Detail"
    button.name="result"
    button.value = element["id"]
    button.type = "button"

    a.appendChild(button)

    tc.make_row([element["id"], element["email"], element["role"], a])
});