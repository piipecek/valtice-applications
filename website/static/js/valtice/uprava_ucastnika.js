import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/uprava_ucastnika/" + id))

console.log(data)

document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("delete_form").submit()
}})