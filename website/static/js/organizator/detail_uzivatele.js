import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"
let id_usera = document.getElementById("id_getter").value
let detail_usera = JSON.parse(httpGet("/admin_api/detail_usera/" + String(id_usera)))
let role_uzivatele = JSON.parse(httpGet("/admin_api/role_uzivatele/" + String(id_usera)))
let checkdiv = document.getElementById("check_div")
let save_roles_button = document.getElementById("save_roles_button")
let resut_input = document.getElementById("result")
let form = document.getElementById("form")
let delete_button = document.getElementById("delete_button")

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

let tc = new TableCreator(document.getElementById("parent_div"))

detail_usera.forEach(element => {
    tc.make_row([element["display_name"], element["value"]])
});

for (let role of role_uzivatele) {
    for (let id of ["organizator", "admin", "super_admin"]) {
        if (role == id) {
            document.getElementById(id).checked = true
        }
    }
}

delete_button.addEventListener("click", function () {
    if (confirm("Opravdu chcete smazat uživatele?")) {
        console.log(document.getElementById("delete_form"))
        document.getElementById("delete_form").submit()
    }
})