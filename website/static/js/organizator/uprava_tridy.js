import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/uprava_tridy/" + id))
let lektori = JSON.parse(httpGet("/org_api/seznam_lektoru_pro_upravu_tridy"))

document.getElementById("name_title").innerText = data["short_name_cz"]


for (let lektor of lektori) {
    let option = document.createElement("option")
    option.value = lektor["id"]
    option.innerText = lektor["full_name"]
    document.getElementById("tutor_id").appendChild(option)
}


for (let key in data) {
    document.getElementById(key).value = data[key]
}


document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat třídu?")) {
        document.getElementById("delete_form").submit()
}})
