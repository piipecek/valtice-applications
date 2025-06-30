import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let tridy = JSON.parse(httpGet("/org_api/tridy_pro_seznamy"))

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
        url: "/organizator/seznamy"
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
    label.innerText = trida["long_name_cz"]
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
    document.getElementById("gym").checked = false
    document.getElementById("vs").checked = false
})
document.getElementById("gym").addEventListener("click", function() {
    document.getElementById("jakekoli_ubytko").checked = false
})
document.getElementById("vs").addEventListener("click", function() {
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

    //mnozina

    let mnozina = ""
    if (document.getElementById("interested").checked) {
        mnozina = "interested"
    } else if (document.getElementById("enrolled").checked) {
        mnozina = "enrolled"
    } else if (document.getElementById("all").checked) {
        mnozina = "all"
    } else if (document.getElementById("tutors").checked) {
        mnozina = "tutors"
    }

    // ubytko
    let ubytko = []
    if (document.getElementById("gym").checked) {
        ubytko.push("gym")
    }
    if (document.getElementById("vs").checked) {
        ubytko.push("vs")
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
    let ostatni_ids = ["korekce", "neregistrace", "dar", "poznamka", "chybejici_udaje", "chybejici_hlavni_trida"]
    for (let id of ostatni_ids) {
        if (document.getElementById(id).checked) {
            ostatni.push(id)
        }
    }


    // atributy
    let atributy_ids = [
        "age", 
        "date_of_birth",
        "email", 
        "phone", 
        "is_student", 
        "is_under_16", 
        "passport_number",
        "datetime_created", 
        "is_this_year_participant", 
        "is_ssh_member", 
        "is_active_participant",
        "is_student_of_partner_zus",
        "datetime_class_pick",
        "datetime_registered",
        "datetime_calculation_email",
        "accomodation_type",
        "accomodation_count",
        "musical_education",
        "musical_instrument",
        "repertoire",
        "comment",
        "admin_comment",
        "meals",
        "billing_currency",
        "billing_date_paid",
        "billing_total",
        "billing_gift",
        "billing_classes",
        "billing_meals",
        "billing_accomodation",
        "billing_correction",
        "billing_correction_reason",
        "billing_food_correction",
        "billing_food_correction_reason",
        "billing_accomodation_correction",
        "billing_accomodation_correction_reason",
        "must_change_password_upon_login",
        "confirmed_email",
        "is_locked",
        "parent",
        "children",
        "primary_class",
        "secondary_classes",
        "tutor_travel",
        "tutor_license_plate",
        "tutor_arrival",
        "tutor_departure",
        "tutor_accompanying_names",
        "tutor_address",
        "tutor_bank_account"
    ]
    let atributy = []
    for (let id of atributy_ids) {
        if (document.getElementById(id).checked) {
            atributy.push(id)
        }
    }

    // result
    let result = {
        "tridy": tridy_ids,
        "mnozina": mnozina,
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
    table_creator.make_header(result["headers"])
    for (let row of result["lidi"]) {
        table_creator.make_row(Object.values(row))
    }
    document.getElementById("pocet_ucastniku").innerText = result["lidi"].length
    document.getElementById("maily").innerText = result["emaily"]
}