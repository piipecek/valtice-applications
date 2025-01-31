import http_get from "../http_get.js"

document.getElementById("logs").innerHTML = JSON.parse(http_get("/admin_api/app_logs"))
