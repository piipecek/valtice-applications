import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/ucastnik/" + id))

console.log(data)
let full_name = data["jmeno"] + " " + data["prijmeni"]
document.getElementById("full_name").innerText = full_name

for (let key in data) {
    console.log(key, data[key])
    if (["jmeno", "prijmeni"].includes(key)) {
        continue
    } else if(["hlavni_trida_1", "hlavni_trida_2", "vedlejsi_trida_placena", "vedlejsi_trida_zdarma"].includes(key)){
        if (data[key]["link"]) {
            let a = document.createElement("a")
            a.href = data[key]["link"]
            a.innerText = data[key]["name"]
            document.getElementById(key).appendChild(a)
        } else {
            document.getElementById(key).innerText = data[key]["name"]
        }
        continue
    }
    document.getElementById(key).innerText = data[key]
}


document.getElementById("smazat_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("smazat_form").submit()
}})