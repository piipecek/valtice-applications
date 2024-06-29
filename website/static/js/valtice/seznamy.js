import httpGet from "../http_get.js"
let tridy = JSON.parse(httpGet("/valtice_api/tridy_pro_seznamy"))

for (let trida of tridy) {
    let input = document.createElement("input")
    input.setAttribute("class", "form-check-input")
    input.setAttribute("type", "checkbox")
    input.setAttribute("value", trida.id)
    input.setAttribute("name", "trida")
    input.setAttribute("id", trida.id)
    input.addEventListener("change", function() {
        document.getElementById("jakakoli_trida").checked = false
    })
    let label = document.createElement("label")
    label.setAttribute("class", "form-check-label")
    label.setAttribute("for", trida.id)
    label.innerText = trida["long_name"]
    let div = document.createElement("div")
    div.setAttribute("class", "form-check")
    div.appendChild(input)
    div.appendChild(label)
    document.getElementById("checkboxy_trid").appendChild(div)
}

// samo-vypinani klikatek o cemkoli
document.getElementById("jakakoli_trida").addEventListener("change", function() {
    for (let trida of tridy) {
        document.getElementById(trida.id).checked = false
    }
})
document.getElementById("jakekoli_ubytko").addEventListener("click", function() {
    document.getElementById("telocvicna").checked = false
    document.getElementById("internat").checked = false
})
document.getElementById("telocvicna").addEventListener("click", function() {
    document.getElementById("jakekoli_ubytko").checked = false
})
document.getElementById("internat").addEventListener("click", function() {
    document.getElementById("jakekoli_ubytko").checked = false
})
let strava_ids = ["snidane_zs", "snidane_vs", "obed_zs", "obed_vs", "vecere_zs", "vecere_vs"]
document.getElementById("jakakoli_strava").addEventListener("click", function() {
    for (let strava_id of strava_ids) {
        document.getElementById(strava_id).checked = false
    }
})
for (let strava_id of strava_ids) {
    document.getElementById(strava_id).addEventListener("click", function() {
        document.getElementById("jakakoli_strava").checked = false
    })
}

// vyhodnocovani
document.getElementById("excel_button").addEventListener("click", function() {vyhodnotit("excel")})
document.getElementById("pdf_button").addEventListener("click", function() {vyhodnotit("pdf")})

function vyhodnotit(forma_vysledku) {
    // tridy
    let tridy_ids = []
    for (let trida of tridy) {
        if (document.getElementById(trida.id).checked) {
            tridy_ids.push(trida.id)
        }
    }

    // ubytko
    let ubytko = []
    if (document.getElementById("telocvicna").checked) {
        ubytko.push("telocvicna")
    }
    if (document.getElementById("internat").checked) {
        ubytko.push("internat")
    }

    // strava
    let strava = []
    for (let strava_id of strava_ids) {
        if (document.getElementById(strava_id).checked) {
            strava.push(strava_id)
        }
    }

    // atributy
    let atributy_ids = ["jmeno", "prijmeni", "cas", "vek", "email", "telefon", "finance_dne", "finance_dar", "finance_mena", "finance_kategorie", "finance_korekce_kurzovne", "finance_korekce_kurzovne_duvod", "finance_korekce_strava", "finance_korekce_strava_duvod", "finance_korekce_ubytko", "finance_korekce_ubytko_duvod", "ssh_clen", "ucast", "hlavni_trida_1_id", "hlavni_trida_2_id", "vedlejsi_trida_placena_id", "vedlejsi_trida_zdarma_id", "ubytovani", "ubytovani_pocet", "vzdelani", "nastroj", "repertoir", "student_zus_valtice_mikulov", "strava", "uzivatelska_poznamka", "admin_poznamka", "cas_registrace"]
    let atributy = []
    for (let id of atributy_ids) {
        if (document.getElementById(id).checked) {
            atributy.push(id)
        }
    }

    // result
    let result = {
        "forma_vysledku": forma_vysledku,
        "tridy": tridy_ids,
        "ubytko": ubytko,
        "strava": strava,
        "atributy": atributy
    }
    document.getElementById("result").value = JSON.stringify(result)
    console.log(result)
    // document.getElementById("form").submit()
}