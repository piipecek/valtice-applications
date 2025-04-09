import httpGet from "../http_get.js"
let data = JSON.parse(httpGet("/user_api/uprava_uctu"))
let jidla = JSON.parse(httpGet("/user_api/jidla_pro_upravu_ucastnika"))


for (let key in data) {
    if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            document.getElementById(key).value = data[key]
        }
    } else if (key == "zmena_ucasti") {
        if (data[key] == "povolena") {
            document.getElementById("zmena_ucasti_povolena").hidden = false
            document.getElementById("zmena_ucasti_zakazana").hidden = true
        } else {
            document.getElementById("zmena_ucasti_povolena").hidden = true
            document.getElementById("zmena_ucasti_zakazana").hidden = false
        }
    } else if (key == "zmena_kategorie") {
        if (data[key] == "povolena") {
            document.getElementById("zmena_kategorie_povolena").hidden = false
            document.getElementById("zmena_kategorie_zakazana").hidden = true
        } else {
            document.getElementById("zmena_kategorie_povolena").hidden = true
            document.getElementById("zmena_kategorie_zakazana").hidden = false
        }
    } else if (key == "has_parent") {
        if (data[key]) {
            document.getElementById("yes_parent").hidden = false
        } else {
            document.getElementById("no_parent").hidden = false
        }
    } else if (key == "manager_name") {
        document.getElementById("manager_name").innerText = data[key]
    } else if (key == "children") {
        if (data[key].length == 0) {
            document.getElementById("children").innerText = "-"
        } else {
            for (let child of data[key]) {
                let child_button = document.createElement("button")
                child_button.innerText = child["full_name"] + " - osamostatnit"
                child_button.classList.add("custom_button", "my-1")
                child_button.type = "button"
                child_button.name = "unlink_child"
                child_button.value = child["id"]

                child_button.addEventListener("click", function() {
                    if (confirm("Opravdu si přejete tento účet osamostatnit?")) {
                        document.getElementById("unlink_child_id").value = child["id"]
                        document.getElementById("unlink_form").submit()
                    }
                })

                document.getElementById("children").appendChild(child_button)
                document.getElementById("children").appendChild(document.createElement("br"))
            }
            document.getElementById("children").lastChild.remove()
        }
    } else if (key == "meals") {
        for (let jidlo of data[key]) {
            add_meal_row(jidlo["meal_id"], jidlo["count"])
        }
    } else if (key == "accomodation_type") {
        
        if (data[key]) {
            document.getElementById("accomodation_type").value = data[key]
        } else {
            // bude tam default select
        }
    } else {
        document.getElementById(key).value = data[key]
    }
}


// skryvani a zobrazovani formulare pro jidlo
function update_meals_visibility() {
    if (document.getElementById("wants_meal").value == "ano") {
        document.getElementById("strava_yes").hidden = false
    } else {
        document.getElementById("strava_yes").hidden = true
    }
}

document.getElementById("wants_meal").addEventListener("change", update_meals_visibility)
update_meals_visibility() // pri nacteni

// nove jidlo a generovani jidel co uz jsou

document.getElementById("add_meal").addEventListener("click", () => {
    add_meal_row(null, 1)
})

function add_meal_row(selected_id, count) {
    let row = document.createElement("div")
    document.getElementById("meals").appendChild(row)
    row.classList.add("row", "my-1")

    let col1 = document.createElement("div")
    row.appendChild(col1)
    col1.className = "col"

    let col2 = document.createElement("div")
    row.appendChild(col2)
    col2.className = "col-auto"

    let col3 = document.createElement("div")
    row.appendChild(col3)
    col3.className = "col-auto"

    let meal_select = document.createElement("select")
    col1.appendChild(meal_select)
    meal_select.name = "meals"
    meal_select.className = "form-control"

    let option = document.createElement("option")
    option.value = "-"
    option.innerText = "-"
    meal_select.appendChild(option)

    for (let jidlo of jidla) {
        let option = document.createElement("option")
        option.value = jidlo["id"]
        option.innerText = jidlo["description"]
        meal_select.appendChild(option)
    }
    if (selected_id) {
        meal_select.value = selected_id
    }

    let count_input = document.createElement("input")
    col2.appendChild(count_input)
    count_input.type = "number"
    count_input.className = "form-control"
    count_input.name = "counts"
    count_input.placeholder = "Počet sad"
    count_input.value = count

    let remove_button = document.createElement("button")
    col3.appendChild(remove_button)
    remove_button.type = "button"
    remove_button.className = "custom_button"
    remove_button.innerText = "Odebrat"
    remove_button.addEventListener("click", () => {
        row.remove()
    })
}