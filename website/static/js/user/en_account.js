import httpGet from "../http_get.js"
let data = JSON.parse(httpGet("/user_api/en_ucet"))


for (let key in data) {
    if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            document.getElementById(key).innerText = data[key]
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
            document.getElementById(key).innerText = "-"
        } else {
            for (let child of data["children"]) {
                let child_button = document.createElement("button")
                child_button.innerText = child["full_name"]
                child_button.classList.add("custom_button", "my-1")
                child_button.type = "submit"
                child_button.name = "child_id"
                child_button.value = child["id"]
                child_button.innerText = "Log-in as " + child["full_name"]

                document.getElementById(key).appendChild(child_button)
                document.getElementById(key).appendChild(document.createElement("br"))
            }
            document.getElementById(key).lastChild.remove()
        }
    } else if (key == "parent") {
        document.getElementById(key).innerText = data[key]
        if (data[key] == "-") {
            document.getElementById("parent_hint").hidden = true
        } else {
            document.getElementById("parent_hint").hidden = false
        }
    } else {
        document.getElementById(key).innerText = data[key]
    }
}