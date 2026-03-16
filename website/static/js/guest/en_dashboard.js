import awaitable_custom_fetch from "../awaitable_custom_fetch.js"

let text = await awaitable_custom_fetch("/guest_api/get_en_text")

document.getElementById("text").innerHTML = text

