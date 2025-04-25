import httpGet from "../http_get.js"

let settings = JSON.parse(httpGet("/org_api/settings"))


for (let key in settings) {
    if (key === "users_locked") {
        continue
    } else if (key === "users_can_send_calculations") {
        continue
    } else {
        document.getElementById(key).value = settings[key]
    }
}

let end_of_issem_form = document.getElementById("end_of_issem_form")
let end_of_issem_button = document.getElementById("end_of_issem")

if (settings["users_locked"]) {
    document.getElementById("lock_state").innerText = "Všichni uživatelé mají zamknuté změny na účtech."
    document.getElementById("toggle_lock").innerText = "Odemknout změny"
} else {
    document.getElementById("lock_state").innerText = "Všichni uživatelé mohou své účty upravovat."
    document.getElementById("toggle_lock").innerText = "Zamknout změny"
}

if (settings["users_can_send_calculations"]) {
    document.getElementById("calculations_state").innerText = "Uživatelé mohou sami sobě zaslat kalkulaci."
    document.getElementById("toggle_calculations").innerText = "Zakázat"
} else {
    document.getElementById("calculations_state").innerText = "Uživatelé si nesmí sami zaslat kalkulaci."
    document.getElementById("toggle_calculations").innerText = "Povolit"
}

end_of_issem_button.addEventListener("click", function () {
    if (confirm("Opravdu chcete ukončit ročník? Ujistěte se, že máte uložený export ročníku.")) {
        end_of_issem_form.submit()
    }
})