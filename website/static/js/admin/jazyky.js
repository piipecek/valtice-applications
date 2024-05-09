import http_get from "../http_get.js"
import TableCreator from "../table_creator.js"


let jazyky = JSON.parse(http_get("/admin_api/uprava_jazyku"))
let tc = new TableCreator(document.getElementById("parent_div"))

tc.make_header(["Display jméno", "Systémové jméno", "Počet překladů", "Detail"])
jazyky.forEach(element => {

    let button = document.createElement("button")
    button.classList.add("btn", "custom-button")
    button.innerText = "Detail"
    button.type="submit"
    button.name="detail"
    button.value = element["id"]
    tc.make_row([element["display_name"], element["system_name"], element["number_of_translations"], button])
});