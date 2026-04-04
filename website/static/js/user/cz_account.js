import awaitable_custom_fetch from "../awaitable_custom_fetch.js"
let data = JSON.parse(await awaitable_custom_fetch("/user_api/ucet"))


for (let key in data) {
    if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            document.getElementById(key).innerText = data[key]
        }
    } else if (key == "is_active_participant") {
        document.getElementById(key).innerText = data[key]
        if (data[key] == "aktivní") {
            document.getElementById("billing_primary_class_row").hidden = false
            document.getElementById("billing_secondary_class_row").hidden = false
            document.getElementById("primary_class_row").hidden = false
            document.getElementById("secondary_class_row").hidden = false
        } else{
            document.getElementById("billing_passive_row").hidden = false
            document.getElementById("no_class_row").hidden = false
        }
    } else if (key == "wants_meals") {
        if (data[key]) {
            document.getElementById("strava_yes").hidden = false
        } else {
            document.getElementById("strava_no").hidden = false
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
    } else if (key == "children") {
        if (data["children"] == "-") {
        } else {
            for (let child of data["children"]) {
                let tr = document.createElement("tr")
                let td1 = document.createElement("td")
                td1.innerText = child["full_name"]
                let td2 = document.createElement("td")
                let a = document.createElement("a")
                a.href = "/user/cz_child_account/" + child["id"]
                let button = document.createElement("button")
                button.classList.add("custom_button")
                button.type = "button"
                button.innerText = "Náhled účtu"
                a.appendChild(button)
                td2.appendChild(a)
                tr.appendChild(td1)
                tr.appendChild(td2)
                document.getElementById("children_tbody").appendChild(tr)
            }
        }
    } else if (key == "parent") {
        document.getElementById(key).innerText = data[key]
        if (document.getElementById("parent_hint")) {
            if (data[key] == "-") {
                document.getElementById("parent_hint").hidden = true
            } else {
                document.getElementById("parent_hint").hidden = false
            }
        }
    } else {
        document.getElementById(key).innerText = data[key]
    }
}