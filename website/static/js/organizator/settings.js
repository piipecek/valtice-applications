import httpGet from "../http_get.js"

let settings = JSON.parse(httpGet("/org_api/settings"))

document.getElementById("primary_classes_start_date").value = settings["primary_classes_start_date"]
document.getElementById("primary_classes_start_time").value = settings["primary_classes_start_time"]
document.getElementById("secondary_classes_start_date").value = settings["secondary_classes_start_date"]
document.getElementById("secondary_classes_start_time").value = settings["secondary_classes_start_time"]
document.getElementById("applications_end_date").value = settings["applications_end_date"]
document.getElementById("applications_end_time").value = settings["applications_end_time"]
document.getElementById("text_cz").value = settings["cz_frontpage_text"]
document.getElementById("text_en").value = settings["en_frontpage_text"]
document.getElementById("vs_capacity").value = settings["vs_capacity"]
document.getElementById("gym_capacity").value = settings["gym_capacity"]
document.getElementById("bank_account").value = settings["bank_account"]
let end_of_issem_form = document.getElementById("end_of_issem_form")
let end_of_issem_button = document.getElementById("end_of_issem")

if (settings["users_locked"]) {
    document.getElementById("lock_state").innerText = "Všichni uživatelé mají zamknuté změny na účtech."
    document.getElementById("toggle_lock").innerText = "Odemknout změny"
} else {
    document.getElementById("lock_state").innerText = "Všichni uživatelé mohou své účty upravovat."
    document.getElementById("toggle_lock").innerText = "Zamknout změny"
}

end_of_issem_button.addEventListener("click", function () {
    if (confirm("Opravdu chcete ukončit ročník? Ujistěte se, že máte uložený export ročníku.")) {
        end_of_issem_form.submit()
    }
})