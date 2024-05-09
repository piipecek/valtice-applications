import httpGet from "../http_get.js"

let uuid = document.getElementById("uuid").value
let data = JSON.parse(httpGet("/acga_api/evaluace/" + uuid))
let main_div = document.getElementById("main")
let result_input = document.getElementById("result")
let ulozit_btn = document.getElementById("ulozit")
let odevzdat_btn = document.getElementById("odevzdat")
let form = document.getElementById("form")

for (let q of data) {
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
        textarea.id = q.id
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
            inp.value = i
            inp.type = "radio"
            inp.name = q.id
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
            inp.name = q.id
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

function odeslat(data) {
    var resultString = JSON.stringify(data);
    result_input.value = resultString;
    form.submit();
}

function vytvorit_result_data(data) {
    let result ={}
    for (let q of data) {
        if (q.typ == "otevrena") {
            result[q.id] = document.getElementById(q.id).value
        }
        else if (q.typ == "ciselna") {
            for (let i=1; i<=q.max; i++ ) {
                if (document.getElementById(q.id + "_" + String(i)).checked){
                    result[q.id] = i
                    break
                }
            }
        }
        else if (q.typ == "single") {
            for (let i=0; i<q.choices.length; i++ ) {
                if (document.getElementById(q.id + "_" + String(i)).checked){
                    result[q.id] = i
                    break
                }
            }
        }
        else if (q.typ == "multiple") {
            let values = []
            for (let i=0; i<q.choices.length; i++ ) {
                if (document.getElementById(q.id + "_" + String(i)).checked){
                    values.push(i)
                }
            }
            result[q.id] = values
        }
    }
    return result
}

ulozit_btn.addEventListener('click', function () {
    let result = vytvorit_result_data(data)
    result["akce"] = "ulozit"
    odeslat(result)
});

odevzdat_btn.addEventListener('click', function () {
    if (confirm("Po odevzdání už nepůjde formulář upravovat. Jste si jistí?")) {
        let result = vytvorit_result_data(data)
        result["akce"] = "odevzdat"
        odeslat(result)
    }
});
