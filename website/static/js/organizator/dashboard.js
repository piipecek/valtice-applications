document.getElementById("delete_button").addEventListener("click", () => {
    if(confirm("Opravdu chcete smazat všechny uživatele?")) {
        document.getElementById("form").submit()
}})