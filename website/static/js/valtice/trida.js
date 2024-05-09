import httpGet from "../http_get.js"

let id = document.getElementById("id_getter").value
let data = JSON.parse(httpGet("/valtice_api/trida/" + id))
console.log(data)

document.getElementById("short_name").innerHTML = data["short_name"]
document.getElementById("full_name").innerHTML = data["full_name"]

for(let ucastnik of data.hlavni_ucastnici_1){
    let tr = document.createElement("tr")
    let td = document.createElement("td")
    let a = document.createElement("a")
    a.href = ucastnik["link"]
    a.innerText = ucastnik["name"]
    td.appendChild(a)
    tr.appendChild(td)
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
    document.getElementById("vedlejsi_ucastnici_zdarma").appendChild(tr)
}

document.getElementById("celkem").innerText = data["celkem"]
document.getElementById("prvni_trida_count").innerText = data["prvni_trida_count"]
document.getElementById("druha_trida_count").innerText = data["druha_trida_count"]
document.getElementById("vedlejsi_placena_count").innerText = data["vedlejsi_placena_count"]
document.getElementById("vedlejsi_zdarma_count").innerText = data["vedlejsi_zdarma_count"]