import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/uprava_ucastnika/" + id))
let tridy = JSON.parse(httpGet("/org_api/tridy_pro_upravu_ucastnika"))

for (let trida of tridy) {
    let option = document.createElement("option")
    option.value = trida["id"]
    option.innerText = trida["full_name_cz"]
    document.getElementById("main_class_id_priority_1").appendChild(option)
    document.getElementById("main_class_id_priority_2").appendChild(option.cloneNode(true))
    document.getElementById("secondary_class_id").appendChild(option.cloneNode(true))
}

let full_name = data["name"] + " " + data["surname"]
if (full_name.trim() == "") {
    full_name = "beze jména"
}
document.getElementById("full_name").innerText = full_name


if (data["is_tutor"]) {
    document.getElementById("tutor_yes").hidden = false
} else {
    document.getElementById("tutor_no").hidden = false
}


for (let key in data) {
    if (key == "datetime_registered") {
        if (data[key] == null) {
            document.getElementById(key).innerText = "Zatím neregistrován"
            document.getElementById("registrovat_button").hidden = false
        } else {
            document.getElementById(key).innerText = data[key]
            document.getElementById("zrusit_registraci_button").hidden = false
        }
    } else if (["main_class_id_priority_1", "main_class_id_priority_2", "secondary_class_id"].includes(key)) {
        if (data[key]) {
            document.getElementById(key).value = data[key]
        } else{
            document.getElementById(key).value = "-"
        }
    } else if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            document.getElementById(key).value = data[key]
        }
    } else if (key == "parent") {
        if (data[key]) {
            document.getElementById("parent_yes").hidden = false
            document.getElementById("parent_name").innerText = data[key]["parent_name"]
        } else {
            document.getElementById("parent_no").hidden = false
        }
    } else {
        document.getElementById(key).value = data[key]
    }
}

document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("delete_form").submit()
}})