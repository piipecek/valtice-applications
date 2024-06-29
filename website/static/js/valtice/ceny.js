import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let ceny = JSON.parse(httpGet("/valtice_api/ceny"))

let table_kurzovne = new TableCreator(document.getElementById("table_kurzovne"))
table_kurzovne.make_header(["Název", "Cena v CZK", "Cena v EUR"])
let table_ubytovani = new TableCreator(document.getElementById("table_ubytovani"))
table_ubytovani.make_header(["Název", "Cena v CZK", "Cena v EUR"])
let table_strava = new TableCreator(document.getElementById("table_strava"))
table_strava.make_header(["Název", "Cena v CZK", "Cena v EUR"])

for (let cena of ceny) {
    let row = [cena["display_name"]]
    let czk_input = document.createElement("input")
    czk_input.type = "float"
    czk_input.value = cena["czk"]
    czk_input.name = cena["id"] + "_czk"
    czk_input.classList.add("form-control")

    let eur_input = document.createElement("input")
    eur_input.type = "float"
    eur_input.value = cena["eur"]
    eur_input.name = cena["id"] + "_eur"
    eur_input.classList.add("form-control")

    row.push(czk_input)
    row.push(eur_input)
    if (cena.typ == "kurzovne") {
        table_kurzovne.make_row(row)
    }
    if (cena.typ == "ubytovani") {
        table_ubytovani.make_row(row)
    }
    if (cena.typ == "strava") {
        table_strava.make_row(row)
    }
}
