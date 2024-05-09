import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let acga_jmeno = httpGet("/acga_api/get_acga_jmeno")
let evaluace = JSON.parse(httpGet("/acga_api/get_evaluace_pro_seznam"))

let generovat_button = document.getElementById("generovat")
let pocet_kodu_input = document.getElementById("pocet_kodu")
let vyplnene_div = document.getElementById("vyplnene")
let nevyplnene_div = document.getElementById("nevyplnene")
let vysledek_div = document.getElementById("vysledek")
let vysledek_button = document.getElementById("vysledek_button")
let vysledek_textarea = document.getElementById("vysledek_textarea")
let ukazat_detaily_button = document.getElementById("ukazat_detaily_button")
let vytvorit_form = document.getElementById("vytvorit_form")
let detaily_form = document.getElementById("detaily_form")
let smazat_stare_button = document.getElementById("smazat_stare")
document.getElementById("acga_jmeno").value = acga_jmeno


ukazat_detaily_button.addEventListener("click", function() {
    document.getElementById("detaily").hidden = false
    ukazat_detaily_button.hidden = true
    document.getElementById("detaily_nadpis").hidden = true
})

generovat_button.addEventListener("click", function() {
    let value = pocet_kodu_input.value
    if (!value) {
        alert("Nebylo zadáno platné číslo.")
    } else if (!acga_jmeno) {
        alert("Nemáte vyplněné jméno učitele.")
    } else {
        vytvorit_form.submit()
    }
})

let today = new Date()
let ago = new Date()
ago.setMonth(today.getMonth() - 2)
let formattedDate = ago.toISOString().split('T')[0];
document.getElementById("date").value = formattedDate

smazat_stare_button.addEventListener("click", function() {
    if (confirm("Budou smazány i formuláře, které mohly být rozpracované, ale neodevzdané. Pokračovat?")) {
        detaily_form.submit()
    }
})

// nejdriv je roztridim, pak udelam tabulky
let vyplnene = []
let nevyplnene = []
for (let e of evaluace) {
    if (e.je_odevzdana) {
        vyplnene.push(e)
    } else {
        nevyplnene.push(e)
    }
}

// tlacitka
function create_delete_button(id) {
    let b = document.createElement("button")
    b.classList.add("btn", "btn-danger")
    b.innerText = "Smazat"
    b.type = "submit"
    b.name = "smazat_evaluaci"
    b.value = id
    return b
}

function create_detail_button(id) {
    let b = document.createElement("button")
    b.classList.add("btn", "custom-button")
    b.innerText = "Detail"
    b.type = "submit"
    b.name = "detail"
    b.value = id
    return b
}

// delani tabulek
if (nevyplnene.length == 0) {
    nevyplnene_div.innerText = "Nejsou tu žádné prázdné evaluace. Nově vytvořené se tu zobrazí po obnovení stránky."
} else {
    let tc = new TableCreator(nevyplnene_div)
    tc.make_header(["Datum vytvoření", "Kód", "Smazat"])
    for (let e of nevyplnene) {
        tc.make_row([e.datetime_vytvoreni, e.kod, create_delete_button(e.id)])
    }
}


if (vyplnene.length == 0) {
    vyplnene_div.innerText = "Nejsou tu žádné vyplněné evaluace."
} else {
    let tc = new TableCreator(vyplnene_div)
    tc.make_header(["Datum vytvoření", "Datum odevzdání", "Detail", "Smazat"])
    for (let e of vyplnene) {
        tc.make_row([e.datetime_vytvoreni, e.datetime_odevzdani, create_detail_button(e.id), create_delete_button(e.id)], [0, 1, 0, 0])
    }
}