import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/uprava_ucastnika/" + id))
let tridy = JSON.parse(httpGet("/valtice_api/tridy_pro_upravu_ucastnika"))

for (let trida of tridy) {
    let option = document.createElement("option")
    option.value = trida["id"]
    option.innerText = trida["full_name"]
    document.getElementById("hlavni_trida_1").appendChild(option)
    document.getElementById("hlavni_trida_2").appendChild(option.cloneNode(true))
    document.getElementById("vedlejsi_trida_placena").appendChild(option.cloneNode(true))
    document.getElementById("vedlejsi_trida_zdarma").appendChild(option.cloneNode(true))

}

let full_name = data["jmeno"] + " " + data["prijmeni"]
document.getElementById("full_name").innerText = full_name

for (let key in data) {
    if (key == "cas_registrace") {
        if (data[key] == null) {
            document.getElementById(key).innerText = "Zatím neregistrován"
            document.getElementById("registrovat_button").hidden = false
        } else {
            document.getElementById(key).innerText = data[key]
            document.getElementById("zrusit_registraci_button").hidden = false
        }
    } else if (["hlavni_trida_1", "hlavni_trida_2", "vedlejsi_trida_placena", "vedlejsi_trida_zdarma"].includes(key)) {
        if (data[key]) {
            document.getElementById(key).value = data[key]
        } else{
            document.getElementById(key).value = "-"
        }
    } else {
        document.getElementById(key).value = data[key]
    }
}

document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("delete_form").submit()
}})