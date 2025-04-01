import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/uprava_ucastnika/" + id))
let tridy = JSON.parse(httpGet("/org_api/tridy_pro_upravu_ucastnika"))
let jidla = JSON.parse(httpGet("/user_api/jidla_pro_upravu_ucastnika")) // pouziva se i v user sekci

let secondary_classes_div = document.getElementById("secondary_classes_div")
let add_secondary_class_button = document.getElementById("add_secondary_class")


function generate_class_picker(name) {
    let select = document.createElement("select")
    select.className = "form-control"
    select.name = name
    for (let trida of tridy) {
        let option = document.createElement("option")
        option.value = trida["id"]
        option.innerText = trida["full_name_cz"]
        select.appendChild(option)
    }
    let option = document.createElement("option")
    option.value = "-"
    option.innerText = "-"
    select.appendChild(option)
    select.value = "-"
    return select
}

function generate_secondary_class_row() {
    let row = document.createElement("div")
    row.classList.add("row", "my-1")
    let col1 = document.createElement("div")
    row.appendChild(col1)
    col1.className = "col"
    let col2 = document.createElement("div")
    row.appendChild(col2)
    col2.className = "col-auto"

    let select = generate_class_picker("secondary_classes")
    col1.appendChild(select)
    let remove_button = document.createElement("button")
    remove_button.type = "button"
    remove_button.className = "custom_button"
    remove_button.innerText = "Odebrat"
    remove_button.addEventListener("click", () => {
        row.remove()
    })
    col2.appendChild(remove_button)
    return row
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


add_secondary_class_button.addEventListener("click", () => {
    let row = generate_secondary_class_row()
    secondary_classes_div.appendChild(row)
    let select = row.children[0].children[0]
    select.value = "-"
})


for (let key in data) {
    if (key == "datetime_registered") {
        if (data[key] == null) {
            document.getElementById(key).innerText = "Zatím neregistrován"
            document.getElementById("registrovat_button").hidden = false
        } else {
            document.getElementById(key).innerText = data[key]
            document.getElementById("zrusit_registraci_button").hidden = false
        }
    } else if (key == "primary_class_id") {
        let select = generate_class_picker("primary_class_id")
        select.value = data[key]
        document.getElementById("primary_class_div").appendChild(select)
    } else if (key == "secondary_classes") {
        for (let i = 0; i < data[key].length; i++) {
            let row = generate_secondary_class_row()
            document.getElementById("secondary_classes_div").appendChild(row)
            let select = row.children[0].children[0]
            console.log(data[key][i])
            select.value = data[key][i]
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

// smazani uzivatele
document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("delete_form").submit()
}})


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

// upozorneni na smazani trid pri pasivni ucasti
function has_any_classes(data) {
    return data["primary_class_id"] || data["secondary_classes"].length > 0
}


let is_active_participant_select = document.getElementById("is_active_participant")
is_active_participant_select.addEventListener("change", () => {
    if (is_active_participant_select.value == "passive" && has_any_classes(data)) {
        if (confirm("Nastavením pasivní účasti budou odhlášeny všechny třídy. Opravdu chcete pokračovat?")) {

        } else {
            is_active_participant_select.value = "active"
        }
    }
})

// dovoleni uprav tridy pri pasivni ucasti

function update_class_selection_visibility() {
    let ucast = document.getElementById("is_active_participant").value
    if (ucast == "passive") {
        document.getElementById("vyber_trid_dovolen").hidden = true
        document.getElementById("vyber_trid_zakazan").hidden = false
    } else {
        document.getElementById("vyber_trid_dovolen").hidden = false
        document.getElementById("vyber_trid_zakazan").hidden = true
    }
}

update_class_selection_visibility()

document.getElementById("is_active_participant").addEventListener("change", update_class_selection_visibility)