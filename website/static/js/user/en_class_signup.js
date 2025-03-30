import httpGet from "../http_get.js"

let primary_tridy_a_kapacity = JSON.parse(httpGet("/user_api/en_primary_classes_capacity"))
let secondary_tridy_a_kapacity = JSON.parse(httpGet("/user_api/en_secondary_classes_capacity"))
let hlavni_tridy_div = document.getElementById("hlavni_tridy")
let vedlejsi_tridy_div = document.getElementById("vedlejsi_tridy")


function handle_class_click(class_id, state, is_main) { // state: "enrolled", "available", "full". is_main: true/false
    if (state === "full") {
        alert("This class is full.")
        return
    }
    let url = "/user_api/handle_en_class_click"
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
                alert(response["status"])
                update_div_trid(response["data"])
            } else {
                let text = JSON.parse(xhr.responseText)["status"]
                alert(text)
            }
        }
    }
}


function update_div_trid(trida) {
    for (let typ of ["main", "secondary"]) {
        let id = typ + "_class_" + trida["id"]
        if (document.getElementById(id)) {

            let id = typ + "_class_" + trida["id"]
            let trida_div = document.getElementById(id)
            trida_div.innerHTML = ""

            trida_div.dataset.state = trida["state_"+typ]

            let color_i = document.createElement("i")
            trida_div.appendChild(color_i)

            if (trida["state_"+typ] === "enrolled") {
                color_i.classList.add("fa-regular", "fa-square-check", "trida_enrolled_icon")
            }
            else if (trida["state_"+typ] === "available") {
                color_i.classList.add("fa-solid", "fa-caret-right", "trida_available_icon")
            } else {
                color_i.classList.add("fa-solid", "fa-circle-minus", "trida_full_icon")
            }

            let text = trida["name"]
            if (trida["is_solo"]) {
                text += " (" + trida["places_taken"] +  "/" + trida["capacity"] + ")"
            } else {
                text += " (" + trida["places_taken"] + ")"
            }
            trida_div.innerHTML += text
        }
    }
}


// to cele probiha pouze tehdy, pokud ucastnik je aktivni -> ma tam vyrenderovane ty divy
if (document.getElementById("aktivni_ucast").value === "True") {
    if (hlavni_tridy_div) {
        // hlavní třídy
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
                    if (confirm("Do you really wish to unsubscribe from the class?")) {
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

    } else if (vedlejsi_tridy_div) {
        // vedlejší třídy
        if (secondary_tridy_a_kapacity.length === 0) {
            vedlejsi_tridy_div.innerText = "There are no secondary classes available."
        } else {
            for (let trida of secondary_tridy_a_kapacity) {
                let trida_div = document.createElement("div")
                vedlejsi_tridy_div.appendChild(trida_div)
                trida_div.id = "secondary_class_" + trida["id"]
                trida_div.classList.add("trida_div")
            
                trida_div.dataset.state = trida["state_secondary"]
                trida_div.addEventListener("click", function() {
                    if (trida_div.dataset.state === "full") {
                        handle_class_click(trida["id"], trida_div.dataset.state, false)
                    } else if (trida_div.dataset.state === "enrolled") {
                        if (confirm("Do you really wish to unsubscribe from the class?")) {
                            handle_class_click(trida["id"], trida_div.dataset.state, false)
                        }
                    } else {
                        handle_class_click(trida["id"], trida_div.dataset.state, false)
                    }
                })
            }
            for (let trida of secondary_tridy_a_kapacity) {
                update_div_trid(trida)
            }
        }
    }
}    

