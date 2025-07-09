let lidi = JSON.parse(document.getElementById("data").value)["lidi"]

for (let key of Object.keys(lidi[0]["data"])) {
    let th = document.createElement("th")
    th.innerText = key
    th.setAttribute("class", "th-okynko")
    document.getElementById("header_row").appendChild(th)
}
for (let clovek of lidi) {
    let tr = document.createElement("tr")
    tr.setAttribute("class", "tr-radek")
    for (let key of Object.keys(clovek["data"])) {
        let td = document.createElement("td")
        td.setAttribute("class", "td-okynko")
        td.innerText = clovek["data"][key]
        tr.appendChild(td)
    }
    document.getElementById("body").appendChild(tr)
}