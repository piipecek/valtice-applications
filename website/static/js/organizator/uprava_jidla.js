import httpGet from "../http_get.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/uprava_jidla/" + id))

for (let key in data) {
    document.getElementById(key).value = data[key]
}


document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat jídlo? Bude odebráno od všech, kteří si jej objednali.")) {
        document.getElementById("delete_form").submit()
}})
