let lidi = JSON.parse(document.getElementById("data").value)["lidi"]

for (let key of Object.keys(lidi[0])) {
    let th = document.createElement("th")
    th.innerText = key
    th.setAttribute("class", "th-okynko")
    document.getElementById("header_row").appendChild(th)
}
for (let clovek of lidi) {
    let tr = document.createElement("tr")
    tr.setAttribute("class", "tr-radek")
    for (let key of Object.keys(clovek)) {
        let td = document.createElement("td")
        td.setAttribute("class", "td-okynko")
        td.innerText = clovek[key]
        tr.appendChild(td)
    }
    document.getElementById("body").appendChild(tr)
}