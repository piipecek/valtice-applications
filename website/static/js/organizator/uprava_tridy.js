import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/uprava_tridy/" + id))

document.getElementById("full_name_title").innerText = data["full_name"]

for (let key in data) {
    document.getElementById(key).value = data[key]
}

document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat třídu?")) {
        document.getElementById("delete_form").submit()
}})