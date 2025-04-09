import httpGet from "../http_get.js"

let solove_druhe_tridy_a_kapacity = JSON.parse(httpGet("/user_api/solo_secondary_classes_capacity"))
let bezkapacitni_druhe_tridy_a_kapacity = JSON.parse(httpGet("/user_api/no_capacity_secondary_classes_capacity"))
let casove_exklutzivni_druhe_tridy_a_kapacity = JSON.parse(httpGet("/user_api/time_exclusive_secondary_classes_capacity"))
let solove_druhe_tridy_div = document.getElementById("solo_secondary_classes")
let bezkapacitni_druhe_tridy_div = document.getElementById("no_capacity_secondary_classes")
let casove_exkluzivni_tridy_div = document.getElementById("time_exclusive_classes_div")


function handle_class_click(class_id, state, is_main) { // state: "enrolled", "available", "full". is_main: true/false
    if (state === "full") {
        alert("Třída je plná")
        return
    }
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
                alert(response["cz_status"])
                update_div_trid(response["data"])
            } else {
                let text = JSON.parse(xhr.responseText)["cz_status"]
                alert(text)
            }
        }
    }
}


function update_div_trid(trida) {
    let id = "secondary_class_" + trida["id"]
    if (document.getElementById(id)) {

        let id = "secondary_class_" + trida["id"]
        let trida_div = document.getElementById(id)
        trida_div.innerHTML = ""

        trida_div.dataset.state = trida["state_secondary"]

        let color_i = document.createElement("i")
        trida_div.appendChild(color_i)

        if (trida["state_secondary"] === "enrolled") {
            color_i.classList.add("fa-regular", "fa-square-check", "trida_enrolled_icon")
        }
        else if (trida["state_secondary"] === "available") {
            color_i.classList.add("fa-solid", "fa-caret-right", "trida_available_icon")
        } else {
            color_i.classList.add("fa-solid", "fa-circle-minus", "trida_full_icon")
        }

        let text = trida["cz_name"]
        if (trida["has_capacity"]) {
            text += " (" + trida["places_taken"] +  "/" + trida["capacity"] + ")"
        } else {
            text += " (" + trida["places_taken"] + ")"
        }
        trida_div.innerHTML += text
    }
}


// to cele probiha pouze tehdy, pokud je mozny prihlasovani -> ma tam vyrenderovane ty divy
if (solove_druhe_tridy_div) {
    // sólové třídy
    if (solove_druhe_tridy_a_kapacity.length === 0) {
        solove_druhe_tridy_div.innerText = "Nejsou tu žádné dostupné vedlejší sólové třídy."
    } else {
        for (let trida of solove_druhe_tridy_a_kapacity) {
            let trida_div = document.createElement("div")
            solove_druhe_tridy_div.appendChild(trida_div)
            trida_div.id = "secondary_class_" + trida["id"]
            trida_div.classList.add("trida_div")
        
            trida_div.dataset.state = trida["state_secondary"]
        
            trida_div.addEventListener("click", function() {
                if (trida_div.dataset.state === "full") {
                    handle_class_click(trida["id"], trida_div.dataset.state, false)
                } else if (trida_div.dataset.state === "enrolled") {
                    if (confirm("Opravdu se chcete z třídy odhlásit?")) {
                        handle_class_click(trida["id"], trida_div.dataset.state, false)
                    }
                } else {
                    handle_class_click(trida["id"], trida_div.dataset.state, false)
                }
            })
        }
        for (let trida of solove_druhe_tridy_a_kapacity) {
            update_div_trid(trida)
        }
    }
}

if (bezkapacitni_druhe_tridy_div) {
    // bezkapacitní třídy
    if (bezkapacitni_druhe_tridy_a_kapacity.length === 0) {
        bezkapacitni_druhe_tridy_div.innerText = "Nejsou tu žádné dostupné vedlejší třídy bez kapacity."
    } else {
        for (let trida of bezkapacitni_druhe_tridy_a_kapacity) {
            let trida_div = document.createElement("div")
            bezkapacitni_druhe_tridy_div.appendChild(trida_div)
            trida_div.id = "secondary_class_" + trida["id"]
            trida_div.classList.add("trida_div")
        
            trida_div.dataset.state = trida["state_secondary"]
            trida_div.addEventListener("click", function() {
                if (trida_div.dataset.state === "full") {
                    handle_class_click(trida["id"], trida_div.dataset.state, false)
                } else if (trida_div.dataset.state === "enrolled") {
                    if (confirm("Opravdu se chcete z třídy odhlásit?")) {
                        handle_class_click(trida["id"], trida_div.dataset.state, false)
                    }
                } else {
                    handle_class_click(trida["id"], trida_div.dataset.state, false)
                }
            })
        }
        for (let trida of bezkapacitni_druhe_tridy_a_kapacity) {
            update_div_trid(trida)
        }
    }
}

if (casove_exkluzivni_tridy_div) {
    // časově exkluzivní třídy
    if (casove_exklutzivni_druhe_tridy_a_kapacity.length === 0) {
        casove_exkluzivni_tridy_div.innerText = "Nejsou tu žádné dostupné časově exkluzivní třídy."
    } else {
        for (let trida of casove_exklutzivni_druhe_tridy_a_kapacity) {
            let trida_div = document.createElement("div")
            casove_exkluzivni_tridy_div.appendChild(trida_div)
            trida_div.id = "secondary_class_" + trida["id"]
            trida_div.classList.add("trida_div")
        
            trida_div.dataset.state = trida["state_secondary"]
        
            trida_div.addEventListener("click", function() {
                if (trida_div.dataset.state === "full") {
                    handle_class_click(trida["id"], trida_div.dataset.state, false)
                } else if (trida_div.dataset.state === "enrolled") {
                    if (confirm("Opravdu se chcete z třídy odhlásit?")) {
                        handle_class_click(trida["id"], trida_div.dataset.state, false)
                    }
                } else {
                    handle_class_click(trida["id"], trida_div.dataset.state, false)
                }
            })
        }
        for (let trida of casove_exklutzivni_druhe_tridy_a_kapacity) {
            update_div_trid(trida)
        }
    }
}