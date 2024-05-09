let input_div = document.getElementById("input_div")
let hra_div = document.getElementById("hra_div")
let input = document.getElementById("input")
let input_button = document.getElementById("input_button")
let start_button = document.getElementById("start_button")
let nova_hra__button = document.getElementById("nova_hra_button")
let count = document.getElementById("count")
let topic = document.getElementById("topic")

let temata = []

input_button.addEventListener("click", function() {
    temata.push(input.value)
    input.value = ""
    count.innerText = temata.length
})

start_button.addEventListener("click", function() {
    input_div.hidden = true
    hra_div.hidden = false
    topic.innerText = temata[Math.floor(Math.random() * temata.length)]
})

nova_hra__button.addEventListener("click", function() {
    location.reload()
})