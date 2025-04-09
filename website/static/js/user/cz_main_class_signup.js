import httpGet from "../http_get.js"

let primary_tridy_a_kapacity = JSON.parse(httpGet("/user_api/primary_classes_capacity"))
let hlavni_tridy_div = document.getElementById("tridy")


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
    let id = "main_class_" + trida["id"]
    if (document.getElementById(id)) {

        let trida_div = document.getElementById(id)
        trida_div.innerHTML = ""

        trida_div.dataset.state = trida["state_main"]

        let color_i = document.createElement("i")
        trida_div.appendChild(color_i)

        if (trida["state_main"] === "enrolled") {
            color_i.classList.add("fa-regular", "fa-square-check", "trida_enrolled_icon")
        }
        else if (trida["state_main"] === "available") {
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


// to cele probiha pouze tehdy, pokud se do trid da prihlasi -> jsou tam ty divy
if (hlavni_tridy_div) {
    for (let trida of primary_tridy_a_kapacity) {
        let trida_div = document.createElement("div")
        hlavni_tridy_div.appendChild(trida_div)
        trida_div.id = "main_class_" + trida["id"]
        trida_div.classList.add("trida_div")
    
        trida_div.dataset.state = trida["state_main"]
    
        trida_div.addEventListener("click", function() {
            if (trida_div.dataset.state === "full") {
                handle_class_click(trida["id"], trida_div.dataset.state, true)
            } else if (trida_div.dataset.state === "enrolled") {
                if (confirm("Opravdu se chcete z třídy odhlásit?")) {
                    handle_class_click(trida["id"], trida_div.dataset.state, true)
                }
            } else {
                handle_class_click(trida["id"], trida_div.dataset.state, true)
            }
        })
    }
    for (let trida of primary_tridy_a_kapacity) {
        update_div_trid(trida)
    }
}    

