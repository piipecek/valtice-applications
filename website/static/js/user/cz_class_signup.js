import httpGet from "../http_get.js"

let tridy_a_kapacity = JSON.parse(httpGet("/user_api/cz_classes_capacity"))
let hlavni_tridy_div = document.getElementById("hlavni_tridy")
let vedlejsi_tridy_div = document.getElementById("vedlejsi_tridy")


function handle_class_click(class_id, state, is_main) { // state: "enrolled", "available", "full". is_main: true/false
    let url = "/user_api/handle_class_click"
    let data = {
        "id": class_id,
        "state": state,
        "main_class": is_main
    }
    let xhr = new XMLHttpRequest()
    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.send(JSON.stringify(data))
    xhr.onreadystatechange = function() { 
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText)
                update_div_obou_trid(response)
            } else {
                let text = JSON.parse(xhr.responseText)["status"]
                alert(text)
            }
        }
    }
}


function update_div_obou_trid(trida) {
    // klik na třídu ovlivňuje vzhled main i secondary třídy
    
    let main_id = "main_class_" + trida["id"]
    let secondary_id = "secondary_class_" + trida["id"]
    
    let main_trida_div = document.getElementById(main_id)
    main_trida_div.innerHTML = ""

    let secondary_trida_div = document.getElementById(secondary_id)
    secondary_trida_div.innerHTML = ""

    // state update

    main_trida_div.dataset.state = trida["state_main"]
    secondary_trida_div.dataset.state = trida["state_secondary"]
    

    // barvicka
    let main_color_i = document.createElement("i")
    let secondary_color_i = document.createElement("i")
    main_trida_div.appendChild(main_color_i)
    secondary_trida_div.appendChild(secondary_color_i)

    if (trida["state_main"] === "enrolled") {
        main_color_i.classList.add("fa-regular", "fa-square-check", "trida_enrolled_icon")
    } else if (trida["state_main"] === "available") {
        main_color_i.classList.add("fa-solid", "fa-caret-right", "trida_available_icon")
    } else {
        main_color_i.classList.add("fa-solid", "fa-circle-minus", "trida_full_icon")
    }

    if (trida["state_secondary"] === "enrolled") {
        secondary_color_i.classList.add("fa-regular", "fa-square-check", "trida_enrolled_icon")
    }
    else if (trida["state_secondary"] === "available") {
        secondary_color_i.classList.add("fa-solid", "fa-caret-right", "trida_available_icon")
    } else {
        secondary_color_i.classList.add("fa-solid", "fa-circle-minus", "trida_full_icon")
    }

    // text a kapacita
    let main_text = trida["name"]
    if (trida["is_solo"]) {
        main_text += " (" + trida["places_taken"] +  "/" + trida["capacity"] + ")"
    } else {
        main_text += " (" + trida["places_taken"] + ")"
    }
    main_trida_div.innerHTML += main_text

    let secondary_text = trida["name"]
    if (trida["is_solo"]) {
        secondary_text += " (" + trida["places_taken"] +  "/" + trida["capacity"] + ")"
    } else {
        secondary_text += " (" + trida["places_taken"] + ")"
    }
    secondary_trida_div.innerHTML += secondary_text

    // let text = trida["name"]
    // if (trida["is_solo"]) {
    //     text += " (" + trida["places_taken"] +  "/" + trida["capacity"] + ")"
    // } else {
    //     text += " (" + trida["places_taken"] + ")"
    // }
    // trida_div.innerHTML += text
}

// hlavní třídy
for (let trida of tridy_a_kapacity) {
    let trida_div = document.createElement("div")
    hlavni_tridy_div.appendChild(trida_div)
    trida_div.id = "main_class_" + trida["id"]
    trida_div.classList.add("trida_div")

    trida_div.dataset.state = trida["state_main"]

    trida_div.addEventListener("click", function() {
        if (trida_div.dataset.state === "full") {
            // no nemas klikat na plnou tridu no
        } else if (trida_div.dataset.state === "enrolled") {
            if (confirm("Opravdu se chcete z třídy odhlásit?")) {
                handle_class_click(trida["id"], trida_div.dataset.state, true)
            }
        } else {
            handle_class_click(trida["id"], trida_div.dataset.state, true)
        }
    })
}

// vedlejší třídy
for (let trida of tridy_a_kapacity) {
    let trida_div = document.createElement("div")
    vedlejsi_tridy_div.appendChild(trida_div)
    trida_div.id = "secondary_class_" + trida["id"]
    trida_div.classList.add("trida_div")

    trida_div.dataset.state = trida["state_secondary"]
    trida_div.addEventListener("click", function() {
        if (trida_div.dataset.state === "full") {
            // no nemas klikat na plnou tridu no
        } else if (trida_div.dataset.state === "enrolled") {
            if (confirm("Opravdu se chcete z třídy odhlásit?")) {
                handle_class_click(trida["id"], trida_div.dataset.state, false)
            }
        } else {
            handle_class_click(trida["id"], trida_div.dataset.state, false)
        }
    })
}

for (let trida of tridy_a_kapacity) {
    update_div_obou_trid(trida)
}

