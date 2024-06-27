import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/uprava_ucastnika/" + id))

let full_name = data["jmeno"] + " " + data["prijmeni"]
document.getElementById("full_name").innerText = full_name

for (let key in data) {
    console.log(key)
}

document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("delete_form").submit()
}})