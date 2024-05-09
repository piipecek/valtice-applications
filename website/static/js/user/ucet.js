import httpGet from "../http_get.js"
let detail_usera = JSON.parse(httpGet("/user_api/detail_usera"))

for (let k of Object.keys(detail_usera)) {
        document.getElementById(k).innerText = detail_usera[k]
}