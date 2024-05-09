import httpGet from "../http_get.js"
let role_uzivatele = JSON.parse(httpGet("/admin_api/role_uzivatele/" + parseInt(document.getElementById("id").value)))
let seznam_roli = JSON.parse(httpGet("/admin_api/both_names_of_all_roles"))
let checkdiv = document.getElementById("check")
let btn = document.getElementById("btn")
let resut_input = document.getElementById("result")
let form = document.getElementById("form")

btn.addEventListener("click", vyhodnotit)


function generator_checkeru(role, is_checked) {
    let inp = document.createElement("input")
    inp.classList.add("form-check-input")
    inp.type="checkbox"
    inp.checked = is_checked
    inp.id = role["system_name"]

    let lab = document.createElement("label")
    lab.classList.add("form-check-label")
    lab.for = role["system_name"]
    lab.innerHTML = role["display_name"]

    let di = document.createElement("div")
    di.classList.add("form-check")
    di.appendChild(inp)
    di.appendChild(lab)
    return di

}


for (let role of seznam_roli) {
    let is_checked = role_uzivatele.includes(role["system_name"])
    checkdiv.appendChild(generator_checkeru(role, is_checked))
}

function vyhodnotit() {
    let result = []
    for (let child of checkdiv.childNodes) {
        let inp = child.childNodes[0]
        if (inp.checked) {
            result.push(inp.id)
        }
    }
    resut_input.value = JSON.stringify(result)
    form.submit()
}
