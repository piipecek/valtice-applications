import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let dal_button = document.getElementById("dal")
let pocet_sloupecku
let jazyky_row = document.getElementById("jazyky")
let jazyky = httpGet("user_api/jazyky")



dal_button.addEventListener("click", function() {vytvorit_tabulku()})

function vytvorit_tabulku(pocet_sloupecku) {
    pocet_sloupecku = document.getElementById("pocet_sloupecku").value
    jazyky_row.hidden = false

    for (let i=0; i<pocet_sloupecku; i++) {

    }
}