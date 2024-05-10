import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let ucastnici = JSON.parse(httpGet("/valtice_api/ucastnici"))

let tc = new TableCreator(document.getElementById("parent_div"), true)
tc.make_header(["Jméno", "E-mail", "Telefon", "Hlavní třída", "Detail"])
ucastnici.forEach(element => {
    let button = document.createElement("button")
    button.classList.add("btn", "btn-success")
    button.type = "submit"
    button.innerText = "Detail účastníka"
    button.name="result"
    button.value = element["id"]
    tc.make_row([element["full_name"], element["email"], element["telefon"], element["hlavni_trida_1"], button])
});

document.getElementById("total").innerText = ucastnici.length

document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat všechny uživatele?")) {
        document.getElementById("delete_form").submit()
}})