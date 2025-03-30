import httpGet from "../http_get.js"

let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/detail_jidla/" + id))

for (let key in data) {
    document.getElementById(key).innerText = data[key]
}