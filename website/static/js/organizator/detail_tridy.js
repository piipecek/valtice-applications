import httpGet from "../http_get.js"

let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/org_api/detail_tridy/" + id))

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
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
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
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("secondary_participants").appendChild(tr)
}