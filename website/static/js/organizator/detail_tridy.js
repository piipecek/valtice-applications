import httpGet from "../http_get.js"

let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/detail_tridy/" + id))

let jmeno_th = document.getElementById("jmeno_th")
let cas_th = document.getElementById("cas_th")

document.getElementById("name").innerHTML = data["short_name_cz"]

for (let key in data) {
    if (["primary_participants", "secondary_participants"].includes(key)) {
        continue
    } else if (key === "tutor") {
        if (data["tutor"]["id"]) {
            let a = document.createElement("a")
            a.href = "/organizator/detail_ucastnika/" + data["tutor"]["id"]
            a.innerText = data["tutor"]["name"]
            a.classList.add("link")
            document.getElementById("tutor").appendChild(a)
        } else {
            document.getElementById("tutor").innerText = data["tutor"]["name"]
        }
    } else {
        document.getElementById(key).innerText = data[key]
    }
}

for(let ucastnik of data.primary_participants){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    a.classList.add("link")
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["cas"]
    tr.appendChild(td2)
    // hidden surnaame td for sorting
    let td3 = document.createElement("td")
    td3.innerText = ucastnik["surname"]
    td3.style.display = "none"
    tr.appendChild(td3)
    document.getElementById("primary_participants").appendChild(tr)
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
    document.getElementById("secondary_participants").appendChild(tr)
}


jmeno_th.addEventListener("click", function() {
    // use hidden surname td for sorting
    let rows = document.querySelectorAll("#primary_participants tr")
    let sortedRows = Array.from(rows).sort((a, b) => {
        let surnameA = a.cells[2].innerText
        let surnameB = b.cells[2].innerText
        return surnameA.localeCompare(surnameB)
    })
    let tableBody = document.getElementById("primary_participants")
    tableBody.innerHTML = ""
    sortedRows.forEach(row => tableBody.appendChild(row))
})


cas_th.addEventListener("click", function() {
    let rows = document.querySelectorAll("#primary_participants tr")
    let sortedRows = Array.from(rows).sort((a, b) => {
        let timeA = a.cells[1].innerText
        let timeB = b.cells[1].innerText
        return timeA.localeCompare(timeB)
    })
    let tableBody = document.getElementById("primary_participants")
    tableBody.innerHTML = ""
    sortedRows.forEach(row => tableBody.appendChild(row))
})