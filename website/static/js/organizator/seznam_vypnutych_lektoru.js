import awaitable_custom_fetch from "../awaitable_custom_fetch.js"
import TableCreator from "../table_creator.js"

let vypnuti = JSON.parse(await awaitable_custom_fetch("/org_api/seznam_vypnutych_lektoru"))

let tc = new TableCreator(document.getElementById("parent_div"), true)
tc.make_header(["Jméno", "Telefon", "E-mail", "Role"])

for (let lektor of vypnuti){
    let a = document.createElement("a")
    a.href = "/organizator/detail_ucastnika/" + lektor["id"]
    a.innerText = lektor["full_name"]
    a.classList.add("jmeno-a")
    tc.make_row([a, lektor["phone"], lektor["email"], lektor["role"]])
}