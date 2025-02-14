import httpGet from "../http_get.js"
import TableCreator from "../table_creator.js"


let jidla = JSON.parse(httpGet("/org_api/seznam_jidel"))

let tc = new TableCreator(document.getElementById("parent_div"), true)
tc.make_header(["Typ", "Lokace", "Vegetariánské", "Počet objednaných sad", "Detail"])

for (let jidlo of jidla){
    
    let a = document.createElement("a")
    a.href = "/organizator/detail_jidla/" + jidlo["id"]
    let button = document.createElement("button")
    button.classList.add("custom_button")
    button.innerText = "Detail"
    button.type = "button"
    a.appendChild(button)
    tc.make_row([jidlo["type"], jidlo["location"], jidlo["is_vegetarian"], jidlo["count"], a])
}