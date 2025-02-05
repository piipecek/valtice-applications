import httpGet from "../http_get.js"


let text = httpGet("/guest_api/get_cz_text")

console.log(text)

document.getElementById("text").innerHTML = text

