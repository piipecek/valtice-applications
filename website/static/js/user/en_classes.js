import awaitable_custom_fetch from "../awaitable_custom_fetch.js"
let data = JSON.parse(await awaitable_custom_fetch("/user_api/classes_overview"))
let class_select = document.getElementById("class_select")
let class_info = document.getElementById("class_info")
let class_name = document.getElementById("class_name")
let main_participants = document.getElementById("main_participants")
let secondary_participants = document.getElementById("secondary_participants")

console.log(data)

class_select.addEventListener("change", handle_trida_display)

for (let trida of data) {
    let option = document.createElement("option")
    option.value = trida.id
    option.textContent = trida.full_name_en
    class_select.appendChild(option)
}

function handle_trida_display() {
    if (class_select.value === "") {
        class_info.hidden = true
        return
    }
    let trida = data.find(t => t.id === parseInt(class_select.value))

    console.log(trida)

    class_name.textContent = trida.full_name_en
    main_participants.innerHTML = ""
    secondary_participants.innerHTML = ""
    for (let participant of trida.main_participants) {
        let li = document.createElement("li")
        li.textContent = participant
        main_participants.appendChild(li)
    }

    let last_main_li = document.createElement("li")
    last_main_li.textContent = trida.main_participants_anonymous_en
    main_participants.appendChild(last_main_li)

    for (let participant of trida.secondary_participants) {
        let li = document.createElement("li")
        li.textContent = participant
        secondary_participants.appendChild(li)
    }

    let last_secondary_li = document.createElement("li")
    last_secondary_li.textContent = trida.secondary_participants_anonymous_en
    secondary_participants.appendChild(last_secondary_li)

    class_info.hidden = false
}
