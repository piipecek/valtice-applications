import http_get from "../http_get.js"

let suggestions = JSON.parse(http_get("/admin_api/suggestions"))
let content_div = document.getElementById("content")

function generator(s) { 
    let div = document.createElement("div")
    content_div.appendChild(div)
    div.classList.add("border", "rounded-2", "border-secondary", "my-2", "p-2")

    function row_generator() {

        let row = document.createElement("div")
        row.classList.add("row", "my-1")
        div.appendChild(row)

        let col1 = document.createElement("div")
        row.appendChild(col1)
        col1.classList.add("col-3")
    
        let col2 =document.createElement("div")
        row.appendChild(col2)
        col2.classList.add("col")

        return [col1, col2]

    }

    let cols_array = row_generator()
    cols_array[0].innerHTML = "Autor"
    cols_array[1].innerHTML = s["author"]

    cols_array = row_generator()
    cols_array[0].innerHTML = "Popis:"
    cols_array[1].innerHTML = s["value"]

    cols_array = row_generator()
    cols_array[0].innerHTML = "Stav řešení:"
    let field = document.createElement("input")
    cols_array[1].appendChild(field)
    field.value = s["state"]
    field.name = s["id"]
    field.classList.add("form-control")

    let upravit_button = document.createElement("button")
    div.appendChild(upravit_button)
    upravit_button.innerHTML = "Uložit stav řešení"
    upravit_button.type = "submit"
    upravit_button.value = s["id"]
    upravit_button.name = "ulozit_stav"
    upravit_button.classList.add("btn", "btn-outline-success")

    let smazat_button = document.createElement("button")
    div.appendChild(smazat_button)
    smazat_button.innerHTML = "Smazat záznam o chybě"
    smazat_button.type = "submit"
    smazat_button.value = s["id"]
    smazat_button.name = "smazat_suggestion"
    smazat_button.classList.add("btn", "btn-outline-danger", "mx-2")
}

if (suggestions.length == 0) {
    content_div.innerText = "Žádné připomínky tu nejsou :)"
} else {
    for (let s of suggestions) {
        generator(s)
    }
}

