import httpGet from "../http_get.js"
let id_usera = document.getElementById("id_getter").value
let role_uzivatele = JSON.parse(httpGet("/org_api/role_uzivatele/" + String(id_usera)))
let checkdiv = document.getElementById("check_div")
let save_roles_button = document.getElementById("save_roles_button")
let resut_input = document.getElementById("result")
let form = document.getElementById("form")

save_roles_button.addEventListener("click", function () {
    let result = []
    for (let child of checkdiv.children) {
        let inp = child.children[0]
        if (inp.checked) {
            result.push(inp.id)
        }
    }
    resut_input.value = JSON.stringify(result)
    form.submit()
})

for (let role of role_uzivatele) {
    for (let id of ["tutor", "organiser", "editor", "admin"]) {
        if (role == id) {
            document.getElementById(id).checked = true
        }
    }
}