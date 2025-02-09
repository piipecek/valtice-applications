import httpGet from "../http_get.js"
let data = JSON.parse(httpGet("/user_api/en_uprava_uctu"))

for (let key in data) {
    if (key.includes("tutor")) {
        if (document.getElementById(key)) {
            document.getElementById(key).value = data[key]
        }
    } else if (key == "has_parent") {
        if (data[key]) {
            document.getElementById("yes_parent").hidden = false
        } else {
            document.getElementById("no_parent").hidden = false
        }
    } else if (key == "manager_name") {
        document.getElementById("manager_name").innerText = data[key]
    } else if (key == "children") {
        if (data[key].length == 0) {
            document.getElementById("children").innerText = "-"
        } else {
            for (let child of data[key]) {
                let child_button = document.createElement("button")
                child_button.innerText = child["full_name"] + " - unlink child account"
                child_button.classList.add("custom_button", "my-1")
                child_button.type = "button"
                child_button.name = "unlink_child"
                child_button.value = child["id"]

                child_button.addEventListener("click", function() {
                    if (confirm("Are you sure you want to unlink this child account?")) {
                        document.getElementById("unlink_child_id").value = child["id"]
                        document.getElementById("unlink_form").submit()
                    }
                })

                document.getElementById("children").appendChild(child_button)
                document.getElementById("children").appendChild(document.createElement("br"))
            }
            document.getElementById("children").lastChild.remove()
        }
    } else {
        document.getElementById(key).value = data[key]
    }
}