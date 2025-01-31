import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/ucastnik/" + id))

// jméno
let full_name = data["jmeno"] + " " + data["prijmeni"]
document.getElementById("full_name").innerText = full_name

// věci na očích
document.getElementById("ucast_na_ocich").innerText = data["ucast"]
document.getElementById("strava_na_ocich").innerText = data["strava_na_ocich"]
document.getElementById("ubytovani_na_ocich").innerText = data["ubytovani"]


// ostatní
for (let key in data) {
    if (["jmeno", "prijmeni"].includes(key)) {
        continue
    } else if (key == "cas_registrace") {
        document.getElementById(key).innerText = data[key]
        if (data[key] != "Zatím neregistrován") {
            document.getElementById("zaregistrovat_form").hidden = true
        }
    } else if (key == "email") {
        if (data[key]) {
            let a = document.createElement("a")
            a.href = "mailto:" + data[key]
            a.innerText = data[key]
            document.getElementById(key).appendChild(a)
        } else {
            document.getElementById(key).innerText = "-"
        }
    } else if(["hlavni_trida_1", "hlavni_trida_2", "vedlejsi_trida_placena", "vedlejsi_trida_zdarma"].includes(key)){
        if (data[key]["link"]) {
            let a = document.createElement("a")
            a.href = data[key]["link"]
            a.innerText = data[key]["name"]
            document.getElementById(key).appendChild(a)
        } else {
            document.getElementById(key).innerText = data[key]["name"]
        }
        continue
    } else {
        document.getElementById(key).innerText = data[key]
    }
}