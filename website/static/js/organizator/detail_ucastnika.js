import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/detail_ucastnika/" + id))

// jméno
let full_name = data["name"] + " " + data["surname"]
if (full_name == "- -") {
    full_name = "beze jména"
}
document.getElementById("full_name").innerText = full_name

// věci na očích
document.getElementById("ucast_na_ocich").innerText = data["is_active_participant"]
document.getElementById("strava_na_ocich").innerText = data["meals_top_visible"]
document.getElementById("ubytovani_na_ocich").innerText = data["accomodation_type"]


// ostatní
for (let key in data) {
    if (["name", "surname", "meals_top_visible"].includes(key)) {
        continue
    } else if (key == "datetime_registered") {
        document.getElementById(key).innerText = data[key]
        if (data[key] != "Zatím neregistrován") {
            document.getElementById("zaregistrovat_form").hidden = true
        }
    } else if (key == "email") {
        if (data[key]) {
            let a = document.createElement("a")
            a.href = "mailto:" + data[key]
            a.innerText = data[key]
            a.classList.add("link")
            document.getElementById(key).appendChild(a)
        } else {
            document.getElementById(key).innerText = "-"
        }
    } else if(["hlavni_trida_1", "hlavni_trida_2", "vedlejsi_trida"].includes(key)){
        if (data[key]["link"]) {
            let a = document.createElement("a")
            a.href = data[key]["link"]
            a.innerText = data[key]["name"]
            a.classList.add("link")
            document.getElementById(key).appendChild(a)
        } else {
            document.getElementById(key).innerText = data[key]["name"]
        }
        continue
    } else if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            // TODO dodelat tohle, jestli tam nejsou nejaky special cases
            document.getElementById(key).innerText = data[key]
        }
    } else {
        document.getElementById(key).innerText = data[key]
    }
}