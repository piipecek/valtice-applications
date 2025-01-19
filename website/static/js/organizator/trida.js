import httpGet from "../http_get.js"

let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/trida/" + id))

document.getElementById("full_name").innerHTML = data["full_name"]

for(let ucastnik of data.hlavni_ucastnici_1){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("hlavni_ucastnici_1").appendChild(tr)
}

for(let ucastnik of data.hlavni_ucastnici_2){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("hlavni_ucastnici_2").appendChild(tr)
}

for(let ucastnik of data.vedlejsi_ucastnici_placeni){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("vedlejsi_ucastnici_placeni").appendChild(tr)
}

for(let ucastnik of data.vedlejsi_ucastnici_zdarma){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    td.appendChild(a)
    tr.appendChild(td)
    let td2 = document.createElement("td")
    td2.innerText = ucastnik["ucast"]
    tr.appendChild(td2)
    document.getElementById("vedlejsi_ucastnici_zdarma").appendChild(tr)
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

document.getElementById("celkem").innerText = count_string(data["celkem"])
document.getElementById("prvni_trida_count").innerText = count_string(data["prvni_trida_count"])
document.getElementById("druha_trida_count").innerText = count_string(data["druha_trida_count"])
document.getElementById("vedlejsi_placena_count").innerText = count_string(data["vedlejsi_placena_count"])
document.getElementById("vedlejsi_zdarma_count").innerText = count_string(data["vedlejsi_zdarma_count"])