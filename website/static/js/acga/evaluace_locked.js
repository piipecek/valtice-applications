import httpGet from "../http_get.js"

let uuid = document.getElementById("uuid").value

let data = JSON.parse(httpGet("/acga_api/evaluace_locked/" + uuid))

document.getElementById("name").innerText = data.name
document.getElementById("date").innerText = data.datetime_odevzdani
let main_div = document.getElementById("main")

for (let q of data["data"]) {
    let question_div = document.createElement("div")
    main_div.appendChild(question_div)
    question_div.classList.add("border", "rounded-2", "border-secondary", "my-3", "p-2", "question_div")
    let otazka = document.createElement("p")
    otazka.innerText = q.otazka
    question_div.appendChild(otazka)

    if (q.typ == "otevrena") {
        let textarea = document.createElement("textarea")
        textarea.classList.add("form-control")
        textarea.rows = 4
        textarea.value = q.value
        textarea.disabled = true
        question_div.appendChild(textarea)
    } else if (q.typ == "ciselna") {
        let span_min = document.createElement("span")
        span_min.classList.add("me-3", "italic_popisek")
        span_min.innerText = q.text_min
        question_div.appendChild(span_min)
        for (let i = 1; i <= q.max; i++) {
            let check_div = document.createElement("div")
            check_div.classList.add("form-check", "form-check-inline")
            let inp = document.createElement("input")
            inp.type = "radio"
            inp.disabled = true
            inp.id = q.id +"_" + String(i)
            inp.classList.add("form-check-input")
            let label = document.createElement("label")
            label.innerText = i
            label.for = inp.id
            label.classList.add("form-check-label", "me-2")
            if (i == q.value) {
                inp.checked = true
            }
            check_div.appendChild(label)
            check_div.appendChild(inp)
            question_div.appendChild(check_div)
        }
        let span_max = document.createElement("span")
        span_max.classList.add("ms-3", "italic_popisek")
        span_max.innerText = q.text_max
        question_div.appendChild(span_max)
    } else if (q.typ == "single") {
        for (let i = 0; i < q.choices.length; i++) {
            let inp = document.createElement("input")
            let label = document.createElement("label")
            label.innerText = q.choices[i]
            inp.id = q.id + "_" + String(i)
            label.for = inp.id
            inp.type = "radio"
            inp.disabled = true
            inp.classList.add("form-check-input")
            inp.classList.add("mx-2")
            if (i == q.value) {
                inp.checked = true
            }
            inp.value = i
            question_div.appendChild(inp)
            question_div.appendChild(label)
            question_div.appendChild(document.createElement("br"))
        }
    } else if (q.typ == "multiple") {
        for (let i = 0; i < q.choices.length; i++) {
            let inp = document.createElement("input")
            let label = document.createElement("label")
            label.innerText = q.choices[i]
            inp.id = q.id + "_" + String(i)
            label.for = inp.id
            inp.classList.add("form-check-input")
            inp.type = "checkbox"
            inp.disabled = "disabled"
            inp.classList.add("mx-2")
            if (q.values && q.values.includes(i)) { //TODO tohle && by tu bejt nemelo, je to hotfix
                inp.checked = true
            }
            inp.value = i
            question_div.appendChild(inp)
            question_div.appendChild(label)
            question_div.appendChild(document.createElement("br"))
        }
    }
}