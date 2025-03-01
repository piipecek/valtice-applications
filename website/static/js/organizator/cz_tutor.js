import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"


let tridy = JSON.parse(httpGet("/org_api/cz_my_participants"))
console.log(tridy)

let parent_div = document.getElementById("parent_div")

if (tridy.length == 0) {
    parent_div.innerText = "Nevyučujete žádnou třídu. Pokud je to chyba, sdělte to organizátorům."
} else {
    for (let trida of tridy) {
        let h2 = document.createElement("h2")
        h2.innerText = trida.class_name + " - hlavní účastníci"
        parent_div.appendChild(h2)
        let main_class_div = document.createElement("div")
        parent_div.appendChild(main_class_div)
        
        let main_class_table = new TableCreator(main_class_div)
        main_class_table.make_header(["Jméno", "Email", "Telefon"])
        for (let participant of trida.primary_participants) {
            main_class_table.make_row([participant.full_name, participant.email, participant.phone])
        }
        
        let h2_second = document.createElement("h2")
        h2_second.innerText = trida.class_name + " - vedlejší účastníci"
        parent_div.appendChild(h2_second)
        let second_class_div = document.createElement("div")
        parent_div.appendChild(second_class_div)

        let second_class_table = new TableCreator(second_class_div)
        second_class_table.make_header(["Jméno", "Email", "Telefon"])
        for (let participant of trida.secondary_participants) {
            second_class_table.make_row([participant.full_name, participant.email, participant.phone])
        }

        parent_div.appendChild(document.createElement("hr"))
    }
}

console.log(tridy)