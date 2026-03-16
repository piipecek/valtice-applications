import awaitable_custom_fetch from "../awaitable_custom_fetch.js"
let id = document.getElementById("id_getter").value
let data = JSON.parse(await awaitable_custom_fetch("/org_api/uprava_jidla/" + id))

for (let key in data) {
    document.getElementById(key).value = data[key]
}


document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat jídlo? Bude odebráno od všech, kteří si jej objednali.")) {
        document.getElementById("delete_form").submit()
}})
