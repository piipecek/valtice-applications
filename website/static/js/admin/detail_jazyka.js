import httpGet from "../http_get.js"
let id = document.getElementById("id").value
let detail_jazyka = JSON.parse(httpGet("/admin_api/detail_jazyka/" + String(id)))

document.getElementById("system_name").value = detail_jazyka["system_name"]
document.getElementById("display_name").value = detail_jazyka["display_name"]
document.getElementById("number_of_translations").innerText = detail_jazyka["number_of_translations"]