let ukazat_button = document.getElementById("ukazat")
let result_div = document.getElementById("result")
let count_span = document.getElementById("count")
let date = document.getElementById("date")
let select = document.getElementById("select")
let dny_histogram_canvas = document.getElementById("dny_histogram")

ukazat_button.addEventListener("click", function() {
    document.getElementById("form").hidden = true
    let form_data = new FormData()
    form_data.append("date", date.value)
    form_data.append("type", select.value)
    console.log(select.value)
    $.ajax({
        type: "POST",
        url: "/acga_api/evaluace_statistiky_data",
        data: form_data,
        contentType: false,
        processData: false,
        success: function(data) {
            handle_response(data)
        }
    })
})

let today = new Date()
let ago = new Date()
ago.setMonth(today.getMonth() - 2)
let formattedDate = ago.toISOString().split('T')[0];
document.getElementById("date").value = formattedDate

function handle_response(response) {
    response = JSON.parse(response)
    let otazky = response.otazky
    let count = response.count
    let dny = response.dny
    let pocty_ve_dnech = response.pocty_ve_dnech
    result_div.hidden = false

    // počet odpovědí
    if (count == 0) {
        count_span.innerText = "Tomuto zadání neodpovídají žádné formuláře."
    } else if (count == 1) {
        count_span.innerText = "Jsou tu ukázány souhrnné výsledky jediného formuláře."
    } else {
        count_span.innerText = "Jsou tu ukázány souhrnné výsledky " + String(count) + " formulářů."
    }

    // histogram odevzdávání
    if (count == 0) {
        document.getElementById("dny_histogram_wrapper").hidden = true
    } else {
        let dny_histogram_ctx = dny_histogram_canvas.getContext("2d")
        var dny_histogram = new Chart(dny_histogram_ctx, {
            type: 'bar',
            data: {
                labels: dny,
                datasets: [{
                    label: 'počet odevzdaných formulářů',
                    data: pocty_ve_dnech,
                    backgroundColor: 'rgba(136, 200, 85, 0.4)',
                    borderColor: 'rgba(136, 200, 85, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                responsive: true,
                maintainAspectRatio: true
            }
        });
    }



    // samotné otázky
    for (let zaznam of otazky) {
        let div = document.createElement("div")
        div.classList.add("plot-div")
        result_div.appendChild(div)
        let p = document.createElement("p")
        p.classList.add("otazka")
        p.innerText = zaznam.otazka
        div.appendChild(p)
        if (zaznam.typ == "histogram") {
            let canvas_div_wrapper = document.createElement("div")
            canvas_div_wrapper.classList.add("canvas-div-wrapper")
            let canvas_div = document.createElement("div")
            canvas_div.classList.add("canvas-div")
            div.appendChild(canvas_div_wrapper)
            canvas_div_wrapper.appendChild(canvas_div)
            let canvas = document.createElement("canvas")
            canvas_div.appendChild(canvas)
            var ctx = canvas.getContext('2d');
        
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: zaznam.x,
                    datasets: [{
                        label: 'počet odpovědí',
                        data: zaznam.y,
                        backgroundColor: 'rgba(136, 200, 85, 0.4)',
                        borderColor: 'rgba(136, 200, 85, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: true
                }
            });
        } else if (zaznam.typ == "otevrena") {
            for (let odpoved of zaznam.odpovedi) {
                let odpoved_div = document.createElement("div")
                odpoved_div.classList.add("odpoved-div")
                if (odpoved.trim() != "") {
                    odpoved_div.innerText = odpoved
                    div.appendChild(odpoved_div)
                }
            }
        }
    }
}


