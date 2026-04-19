import awaitable_custom_fetch from "../awaitable_custom_fetch.js"
let id = document.getElementById("child_id").value
let data = JSON.parse(await awaitable_custom_fetch("/user_api/en_child_account/" + id))

let show_finance_button = document.getElementById("show_finance_button")
let finance_show = document.getElementById("finance_calculation")


show_finance_button.addEventListener("click", function() {
    if (confirm("Do you really want to view the calculation of your child? Please do not pay any amounts before the date written above.")) {
        finance_show.hidden = false
        show_finance_button.hidden = true
    }
})


for (let key in data) {
    if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            document.getElementById(key).innerText = data[key]
        }
    } else if (key == "is_locked") {
        document.getElementById(key).innerText = data[key]
        if (data[key] == "Ano") {
            document.getElementById("locked_yes").hidden = false
        } else {
            document.getElementById("locked_no").hidden = false
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