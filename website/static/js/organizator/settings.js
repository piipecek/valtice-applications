import httpGet from "../http_get.js"

let settings = JSON.parse(httpGet("/valtice_api/settings"))

document.getElementById("applications_start_date").value = settings["applications_start_date"]
document.getElementById("applications_start_time").value = settings["applications_start_time"]
document.getElementById("applications_end_date").value = settings["applications_end_date"]
document.getElementById("applications_end_time").value = settings["applications_end_time"]



document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat všechny uživatele?")) {
        document.getElementById("form").submit()
}})