import http_get from "../http_get.js"

let suggestions = JSON.parse(http_get("/guest_api/suggestions"))
let content_div = document.getElementById("content")

if (suggestions.length == 0) {
    content_div.innerText = "Žádná připomínka tu není."
}

for (let s of suggestions) {
    let div = document.createElement("div")
    content_div.appendChild(div)
    div.classList.add("border", "rounded-2", "border-secondary", "my-2", "p-2", "suggestion")
    div.classList.add("bug")

    function row_generator() {

        let row = document.createElement("div")
        row.classList.add("row", "my-1")
        div.appendChild(row)

        let col1 = document.createElement("div")
        row.appendChild(col1)
        col1.classList.add("col-2")
    
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
    cols_array[1].innerHTML = s["state"]
}