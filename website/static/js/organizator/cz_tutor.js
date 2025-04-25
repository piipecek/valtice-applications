import httpGet from "../http_get.js"

let tridy = JSON.parse(httpGet("/org_api/cz_my_participants"))

let parent_div = document.getElementById("parent_div")


function row_factory(label, value) {
    let row = document.createElement("div")
    row.classList.add("row")
    let label_div = document.createElement("div")
    label_div.classList.add("col-sm-3")
    label_div.innerText = label
    label_div.classList.add("tutor-name-label")
    let value_div = document.createElement("div")
    value_div.classList.add("col-sm")
    value_div.innerText = value
    row.appendChild(label_div)
    row.appendChild(value_div)
    return row
}


if (tridy.length == 0) {
    parent_div.innerText = "Nevyučujete žádnou třídu. Pokud je to chyba, sdělte to organizátorům."
} else {
    for (let trida of tridy) {

        parent_div.appendChild(document.createElement("hr"))

        let h2 = document.createElement("h2")
        h2.innerText = trida.class_name + " - hlavní účastníci"
        parent_div.appendChild(h2)
        let main_class_div = document.createElement("div")
        parent_div.appendChild(main_class_div)
        
        for (let participant of trida.primary_participants) {
            let participant_div = document.createElement("div")
            parent_div.appendChild(participant_div)
            participant_div.classList.add("tutor-participant-div")
            console.log(participant)
            console.log(participant.full_name_cz)
            participant_div.appendChild(row_factory("Jméno", participant.full_name_cz))
            participant_div.appendChild(row_factory("E-mail", participant.email))
            participant_div.appendChild(row_factory("Telefon", participant.phone))
            participant_div.appendChild(row_factory("Věk", participant.age))
            participant_div.appendChild(row_factory("Hudební vzdělání", participant.education))
            participant_div.appendChild(row_factory("Repertoár", participant.repertoire))
            participant_div.appendChild(row_factory("Čas přihlášení do třídy", participant.datetime_class_pick))
        }

        parent_div.appendChild(document.createElement("hr"))

        let h2_second = document.createElement("h2")
        h2_second.innerText = trida.class_name + " - vedlejší účastníci"
        parent_div.appendChild(h2_second)
        let second_class_div = document.createElement("div")
        parent_div.appendChild(second_class_div)

        for (let participant of trida.secondary_participants) {
            let participant_div = document.createElement("div")
            parent_div.appendChild(participant_div)
            participant_div.classList.add("tutor-participant-div")
            
            participant_div.appendChild(row_factory("Jméno", participant.full_name_cz))
            participant_div.appendChild(row_factory("E-mail", participant.email))
            participant_div.appendChild(row_factory("Telefon", participant.phone))
            participant_div.appendChild(row_factory("Věk", participant.age))
            participant_div.appendChild(row_factory("Hudební vzdělání", participant.education))
            participant_div.appendChild(row_factory("Repertoár", participant.repertoire))
            participant_div.appendChild(row_factory("Čas přihlášení do třídy", participant.datetime_class_pick))
        }

    }
}