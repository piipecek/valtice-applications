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
    } else if (key == "is_active_participant") {
        document.getElementById(key).innerText = data[key]
        if (data[key] == "aktivní") {
            document.getElementById("billing_primary_class_row").hidden = false
            document.getElementById("billing_secondary_class_row").hidden = false
        } else{
            document.getElementById("billing_passive_row").hidden = false
        }
    } else if (key == "is_tutor") {
        if (data[key]) {
            document.getElementById("tutor_yes").hidden = false
        } else {
            document.getElementById("tutor_no").hidden = false
        }
    } else if (key == "wants_meals") {
        if (data[key]) {
            document.getElementById("strava_yes").hidden = false
            let food_ids = ["billing_snidane_row", "billing_obedy_row", "billing_vecere_row"]
            for (let id of food_ids) {
                document.getElementById(id).hidden = false
            }
        } else {
            document.getElementById("strava_no").hidden = false
            document.getElementById("billing_strava_row").hidden = false
        }
    } else if (key == "meals") {
        for (let meal of data[key]) {
            let tr = document.createElement("tr")
            let td1 = document.createElement("td")
            td1.innerText = meal["popis"]
            let td2 = document.createElement("td")
            td2.innerText = meal["count"]
            tr.appendChild(td1)
            tr.appendChild(td2)
            document.getElementById("meals").appendChild(tr)
        }
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
    } else if(["hlavni_trida", "vedlejsi_trida"].includes(key)){
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
            document.getElementById(key).innerText = data[key]
        }
    } else if (key == "taught_classes") {
        let links_span = document.createElement("span")
        if (data["taught_classes"].length == 0) {
            links_span.innerText = "Žádné"
        } else {
            for (let trida of data["taught_classes"]) {
                let trida_a = document.createElement("a")
                trida_a.href = "/organizator/detail_tridy/" + trida["id"]
                trida_a.innerText = trida["short_name"]
                trida_a.classList.add("link")
                links_span.appendChild(trida_a)
                links_span.appendChild(document.createTextNode(", "))
            }
            links_span.lastChild.remove()
        }
        document.getElementById(key).appendChild(links_span)
    } else if (key == "parent") {
        if (data["parent"] == "-") {
            document.getElementById(key).innerText = "-"
        } else {
            let parent_a = document.createElement("a")
            parent_a.href = "/organizator/detail_ucastnika/" + data["parent"]["parent_id"]
            parent_a.innerText = data["parent"]["parent_name"]
            parent_a.classList.add("link")
            document.getElementById(key).appendChild(parent_a)
        }
    } else if (key == "children") {
        if (data["children"] == "-") {
            document.getElementById(key).innerText = "-"
        } else {
            for (let child of data["children"]) {
                let child_a = document.createElement("a")
                child_a.href = "/organizator/detail_ucastnika/" + child["child_id"]
                child_a.innerText = child["child_name"]
                child_a.classList.add("link")
                document.getElementById(key).appendChild(child_a)
                document.getElementById(key).appendChild(document.createTextNode(", "))
            }
            document.getElementById(key).lastChild.remove()
        }
    } else {
        document.getElementById(key).innerText = data[key]
    }
}