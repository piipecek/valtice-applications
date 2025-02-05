import httpGet from "../http_get.js"


let text = httpGet("/guest_api/get_en_text")

document.getElementById("text").innerHTML = text

