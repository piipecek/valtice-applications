import httpGet from "../http_get.js"

let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/detail_tridy/" + id))

document.getElementById("name").innerHTML = data["short_name_cz"]

for (let key in data) {
    if (["main_participants_priority_1", "main_participants_priority_2", "secondary_participants"].includes(key)) {
        continue
    } else {
        document.getElementById(key).innerText = data[key]
    }
}

for(let ucastnik of data.main_participants_priority_1){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    a.classList.add("link")
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("main_participants_1").appendChild(tr)
}

for(let ucastnik of data.main_participants_priority_2){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    a.classList.add("link")
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("main_participants_2").appendChild(tr)
}

for(let ucastnik of data.secondary_participants){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    a.classList.add("link")
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("secondary_participants").appendChild(tr)
}

function count_string(count) {
    if (count == 0) {
        return "Žádní účastníci."
    } else if (count == 1) {
        return "Celkem jeden účastník."
    } else if (count <= 4) {
        return "Celkem "+ String(count) + " účastníci." 
    } else {
        return "Celkem "+String(count)+" účastníků."
    }
}