let textarea = document.getElementById("textarea")
let button = document.getElementById("button")
let download_plot_button = document.getElementById("download_plot")
let download_histogram_button = document.getElementById("download_histogram")
let plot_div = document.getElementById('plot_div')
let histogram_div = document.getElementById('histogram_div')
let result_div = document.getElementById("result")

button.addEventListener("click", main)
download_plot_button.addEventListener("click", download_plot)
download_histogram_button.addEventListener("click", download_histogram)

let plot = null
let histogram = null

function parse() {
    let text = textarea.value
    let lines = text.split("\n")
    let lines_parsed = []
    for (let line of lines) {
        if (line == "") {
            continue
        } else {
            line.replace(", ", ",")
            let new_line = line.split(",")
            if (new_line.length == 2) {
                for (let i = 0; i < new_line.length; i++) {
                    if (new_line[i] == "-") {
                        new_line[i] = null
                    } else {
                        new_line[i] = parseInt(new_line[i]);
                    }
                }
                lines_parsed.push(new_line)
            } else {
                return null
            }
        }
    }
    return lines_parsed
}


function main() {
    result_div.hidden = false
    download_histogram_button.hidden = false
    download_plot_button.hidden = false
    let parsed_input = parse()
    if (parsed_input) {
        ocekavana_vs_obdrzena_plot(parsed_input)
        histogram_plot(parsed_input)
        prumerne_hodnoty(parsed_input)
    } else {
        alert("V zadaných známkách je chyba někde, zkuste jí najít a opravit.")
    }
}

function ocekavana_vs_obdrzena_plot(parsed_input) {
    let data = []
    for (let line of parsed_input){
        if (line.includes(null)) {

        } else {
            data.push({
                "x": line[0],
                "y": line[1]
            })
        }
    }

    // vytvoreni canvasu
    plot_div.innerHTML = null
    let canvas = document.createElement("canvas")
    plot_div.appendChild(canvas)

    // vyska a sirka canvasu
    let vyska = window.outerHeight
    let sirka = window.outerWidth
    if (vyska > sirka) {
        plot_div.style.width = sirka*0.9
    } else {
        plot_div.style.height = vyska*0.9
    }

    let  ctx = canvas.getContext('2d');

    plot = new Chart(ctx, {
        data: {
            datasets: [{
                type: 'scatter',
                label: "Studenti",
                data: data,
                borderColor: "rgb(0,151,10)",
                backgroundColor: "rgb(148,256,148)",
                pointStyle: "cross",
                pointRadius: 8,
                pointHoverRadius: 10,
                borderWidth: 3
              }, {
                type: 'line',
                label: 'y=x',
                data: [{x: 0, y: 0}, {x:100, y:100}],
                pointStyle: false,
                borderColor: "rgb(256,0,0)",
                backgroundColor: "rgb(256,148,148)",
                borderWidth: 1
            }],
        },
        options: {
            aspectRatio: 1.7,
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "Obdržená známka",
                        font: {
                            size: 25
                        }
                    },
                    ticks: {
                        font: {
                            size:20
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Očekávaná známka",
                        font: {
                            size: 25
                        }
                    },
                    ticks: {
                        font: {
                            size:20
                        }
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: "Srovnání očekávaných a obdržených známek",
                    font: {
                        size: 25
                    }
                }
            },
            animation: false
        }
    });
}

function histogram_plot(parsed_input) {
    let data = [0, 0, 0, 0, 0]
    for (let line of parsed_input){
        if (line[1] >= 80) {
            data[0] ++
    
        } else if (line[1] >= 65) {
            data[1] ++
        } else if (line[1] >= 50) {
            data[2] ++
        } else if (line[1] >= 35) {
            data[3] ++
        } else {
            data[4] ++
        }
    }

    // vytvoreni canvasu
    histogram_div.innerHTML = null
    let canvas = document.createElement("canvas")
    histogram_div.appendChild(canvas)

    // vyska a sirka canvasu
    let vyska = window.outerHeight
    let sirka = window.outerWidth
    if (vyska > sirka) {
        histogram_div.style.width = sirka*0.9
    } else {
        histogram_div.style.height = vyska*0.9
    }

    let  ctx = canvas.getContext('2d');

    histogram = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["1", "2", "3", "4", "5"],
            datasets: [{
                data: data,
                backgroundColor: 'rgba(136, 200, 85, 0.4)',
                borderColor: 'rgba(136, 200, 85, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Četnost",
                        font: {
                            size: 25
                        }
                    },
                    ticks: {
                        font: {
                            size:20
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "Známky",
                        font: {
                            size: 25
                        }
                    },
                    ticks: {
                        font: {
                            size:20
                        }
                    }
                }
            },
            animation: false,
            plugins: {
                title: {
                    display: true,
                    text: "Četnost přepočtených známek",
                    font: {
                        size: 25
                    }
                },
                legend: {
                    display: false
                }
            }
        }
    });
}

function prumerne_hodnoty(parsed_input) {
    let ocekavane_znamky = []
    let obdrzene_znamky = []
    for (let line of parsed_input) {
        ocekavane_znamky.push(line[0])
        obdrzene_znamky.push(line[1])
    }
    ocekavane_znamky = ocekavane_znamky.filter(num => num !== null);
   obdrzene_znamky =obdrzene_znamky.filter(num => num !== null);

    let avg_exp_total = 0
    for (let n of ocekavane_znamky) {
        avg_exp_total += n
    }
    let avg_total = 0
    for (let n of obdrzene_znamky) {
        avg_total += n
    }
    document.getElementById("avg_exp").innerText = String(Math.round(avg_exp_total/ocekavane_znamky.length*100)/100).replace(".",",")
    document.getElementById("avg").innerText = String(Math.round(avg_total/obdrzene_znamky.length*100)/100).replace(".",",")
}

function download_plot() {
    let a = document.createElement('a');
    a.href = plot.toBase64Image("image/png", 1);
    a.download = 'plot.png';
    a.click();
}

function download_histogram() {
    let b = document.createElement('a');
    b.href = histogram.toBase64Image("image/png", 1);
    b.download = 'histogram.png';
    b.click();
}
