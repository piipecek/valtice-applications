import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/ucastnik/" + id))

console.log(data)

for (let key in data) {
    if(["hlavni_trida_1", "hlavni_trida_2", "vedlejsi_trida_placena", "vedlejsi_trida_zdarma"].includes(key)){
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
let full_name = data["jmeno"] + " " + data["prijmeni"]
document.getElementById("full_name").innerText = full_name


document.getElementById("smazat_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat uživatele?")) {
        document.getElementById("smazat_form").submit()
}})