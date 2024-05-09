import http_get from "../http_get.js"
import TableCreator from "../table_creator.js"

let roles = JSON.parse(http_get("/admin_api/info_pro_upravu_roli"))

let tc = new TableCreator(document.getElementById("parent_div"))
tc.make_header(["Systémové jméno", "Display jméno", "Počet uživatelů s rolí", "Detail"])
roles.forEach(element => {

    let button = document.createElement("button")
    button.classList.add("btn", "btn-danger")
    button.innerHTML = "Smazat"
    button.name="smazat"
    button.value = element["system_name"]
    tc.make_row([element["system_name"], element["display_name"], element["number_of_users"], button], [0, 1, 0, 0])
});
