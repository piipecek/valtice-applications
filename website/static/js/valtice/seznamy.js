import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let tridy = JSON.parse(httpGet("/valtice_api/tridy_pro_seznamy"))

// togglovani sekci
document.getElementById("vytvorit_button").addEventListener("click", function() {
    document.getElementById("prvni_krok").hidden = true
    document.getElementById("loader").hidden = false
    $.ajax({
        data : {
            ucel: "view",
            result: JSON.stringify(vyhodnotit())
        },
        type: "POST",
        url: "/valtice/seznamy"
    })
    .done(function(data) {
        document.getElementById("loader").hidden = true
        document.getElementById("druhy_krok").hidden = false
        vykreslit_tabulku(JSON.parse(data))
    })
    .fail(function() {
        alert("Něco se nepovedlo")
    })
})
document.getElementById("ukazat_parametry").addEventListener("click", function() {
    document.getElementById("prvni_krok").hidden = false
    document.getElementById("druhy_krok").hidden = true
})


// vytvoreni checkboxu trid
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

document.getElementById("excel_button").addEventListener("click", function() {
    document.getElementById("data").value = JSON.stringify(vyhodnotit())
    document.getElementById("ucel").value = "excel"
    document.getElementById("form").submit()
})
document.getElementById("pdf_button").addEventListener("click", function() {
    document.getElementById("data").value = JSON.stringify(vyhodnotit())
    document.getElementById("ucel").value = "pdf"
    document.getElementById("form").submit()
})

function vyhodnotit() {
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
        ubytko.push("Tělocvična")
    }
    if (document.getElementById("internat").checked) {
        ubytko.push("Internát vinařské školy")
    }

    // strava
    let strava = []
    for (let strava_id of strava_ids) {
        if (document.getElementById(strava_id).checked) {
            strava.push(strava_id)
        }
    }

    // ostatni
    let ostatni = []
    let ostatni_ids = ["korekce", "neregistrace", "dar", "poznamka"]
    for (let id of ostatni_ids) {
        if (document.getElementById(id).checked) {
            ostatni.push(id)
        }
    }


    // atributy
    let atributy_ids = ["cas", "vek", "email", "telefon", "finance_dne", "finance_celkem", "finance_dar", "finance_mena", "finance_kategorie", "finance_kurzovne", "finance_strava", "finance_ubytovani", "finance_korekce_kurzovne", "finance_korekce_kurzovne_duvod", "finance_korekce_strava", "finance_korekce_strava_duvod", "finance_korekce_ubytko", "finance_korekce_ubytko_duvod", "ssh_clen", "ucast", "hlavni_trida_1_id", "hlavni_trida_2_id", "vedlejsi_trida_placena_id", "vedlejsi_trida_zdarma_id", "ubytovani", "ubytovani_pocet", "vzdelani", "nastroj", "repertoir", "student_zus_valtice_mikulov", "strava", "uzivatelska_poznamka", "admin_poznamka", "cas_registrace"]
    let atributy = []
    for (let id of atributy_ids) {
        if (document.getElementById(id).checked) {
            atributy.push(id)
        }
    }

    // result
    let result = {
        "tridy": tridy_ids,
        "ubytko": ubytko,
        "strava": strava,
        "ostatni": ostatni,
        "atributy": atributy,
        "atribut_razeni": document.getElementById("atribut_razeni").value,
    }
    return result
}

function vykreslit_tabulku(result) {
    let table_creator = new TableCreator(document.getElementById("parent_div"), true, true)
    let header = Object.keys(result["lidi"][0])
    table_creator.make_header(header)
    for (let row of result["lidi"]) {
        table_creator.make_row(Object.values(row))
    }
    document.getElementById("pocet_ucastniku").innerText = result["lidi"].length
    document.getElementById("maily").innerText = result["emaily"]
}