import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"

let users_from_db = JSON.parse(httpGet("/admin_api/admin_users_from_db"))
let tc = new TableCreator(document.getElementById("parent_div"))

tc.make_header(["#", "E-mail", "Poslední přihlášení", "Confirmed", "Detail"])
users_from_db.forEach(element => {
    let button = document.createElement("button")
    button.classList.add("btn", "btn-success")
    button.type = "submit"
    button.innerText = "Detail usera"
    button.name="result"
    button.value = element["id"]
    tc.make_row([element["id"], element["email"], element["last_login_datetime"], element["confirmed"], button])
});