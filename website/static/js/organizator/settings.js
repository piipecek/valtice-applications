import httpGet from "../http_get.js"

let settings = JSON.parse(httpGet("/org_api/settings"))

document.getElementById("applications_start_date").value = settings["applications_start_date"]
document.getElementById("applications_start_time").value = settings["applications_start_time"]
document.getElementById("applications_end_date").value = settings["applications_end_date"]
document.getElementById("applications_end_time").value = settings["applications_end_time"]
document.getElementById("text_cz").value = settings["cz_frontpage_text"]
document.getElementById("text_en").value = settings["en_frontpage_text"]