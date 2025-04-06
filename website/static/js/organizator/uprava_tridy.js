import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/uprava_tridy/" + id))
let lektori = JSON.parse(httpGet("/org_api/seznam_lektoru_pro_upravu_tridy"))
let has_capacity_select = document.getElementById("has_capacity")
let capacity_row = document.getElementById("capacity_row")

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

function update_capacity_visibility() {
    if (has_capacity_select.value === "Ano") {
        capacity_row.hidden = false
    } else {
        capacity_row.hidden = true
    }
}

has_capacity_select.addEventListener("change", update_capacity_visibility)

update_capacity_visibility()