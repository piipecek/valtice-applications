import csvToObjectArray from "./vydaje_helpers.js"


// file inputs
let csv_file_input = document.getElementById('csvFileInput')
let pravidla_file_input = document.getElementById("pravidlaFileInput")

// buttony
let jsem_tu_nove_button = document.getElementById("jsem_tu_nove_button")
let mam_pravidla_button = document.getElementById("mam_pravidla_button")
let stahnout_pravidla_button = document.getElementById("stahnout_pravidla")
let nove_pravidlo_button = document.getElementById("nove_pravidlo")
let prepocitat_button = document.getElementById("prepocitat_button")

// containery
let pravidla_buttons_div = document.getElementById("pravidla_buttons")
let nahrat_pravidla_div = document.getElementById("nahrat_pravidla")
let pravidla_div = document.getElementById("pravidla_div")
let main_table = document.getElementById("main_table")
let main_div = document.getElementById("main_div")
let pravidla_table = document.getElementById("pravidla")
let nahrat_csv_div = document.getElementById("nahrat_csv_div")
let result_div = document.getElementById("result")
let main_plot_div = document.getElementById("main_plot_div")

// inputs na nove pravidlo
let udaj_select = document.getElementById("udaj_select")
let vyskyt_select = document.getElementById("vyskyt_select")
let klic_input = document.getElementById("klic_input")
let kategorie_select = document.getElementById("kategorie_select")
let kategorie_input = document.getElementById("kategorie_input")

// optiony
let zprava_option = document.getElementById("zprava_option")
let cislo_protiuctu_option = document.getElementById("cislo_protiuctu_option")
let je_option = document.getElementById("je_option")

//others
let count_span = document.getElementById("count")
let datum_sort = document.getElementById("datum_sort")
let castka_sort = document.getElementById("castka_sort")
let misto_sort = document.getElementById("misto_sort")
let datum_sort_span = document.getElementById("datum_sort_span")
let castka_sort_span = document.getElementById("castka_sort_span")
let misto_sort_span = document.getElementById("misto_sort_span")


// arrays
let vsechny_platby = []
let roztrizene_platby = []
let celkova_suma = 0

// Function to display the objects in the HTML
function display_zbyle_vydaje(objects) {
    main_div.hidden = ""
    nahrat_csv_div.hidden = "hidden"
    main_table.innerHTML = '';
    count_span.innerText = objects.length

    for (const obj of objects) {
        let tr = document.createElement("tr")
        let td1 = document.createElement("td")
        let td2 = document.createElement("td")
        let td3 = document.createElement("td")
        let td4 = document.createElement("td")
        let td5 = document.createElement("td")
        td1.innerText = obj["datum zaúčtování"]
        td2.innerText = obj["castka"].toFixed(2).replace(".", ",") + "\u00A0Kč"
        td3.innerText = obj["misto"]
        td4.innerText = obj["číslo protiúčtu"]
        td5.innerText = obj["zpráva"]
        td4.classList.add("hover-blue")
        td5.classList.add("hover-blue")
        td4.addEventListener("click", function() {
            cislo_protiuctu_option.selected = "selected"
            je_option.selected = "selected"
            klic_input.value = obj["číslo protiúčtu"]
            prepsat_shodnost()
        })
        td5.addEventListener("click", function() {
            zprava_option.selected = "selected"
            je_option.selected = "selected"
            klic_input.value = obj["zpráva"]
            prepsat_shodnost()
        })
        tr.appendChild(td1)
        tr.appendChild(td2)
        tr.appendChild(td3)
        tr.appendChild(td4)
        tr.appendChild(td5)
        main_table.appendChild(tr)
        
    }
}

function display_pravidlo(udaj, vyskyt, klic, kategorie) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    let td4 = document.createElement("td")
    let td5 = document.createElement("td")
    td1.innerText = udaj
    td2.innerText = vyskyt
    td3.innerText = klic
    td4.innerText = kategorie
    let b = document.createElement("button")
    b.classList.add("btn", "btn-danger")
    b.innerText = "Smazat pravidlo"
    b.addEventListener("click", function() {
        tr.remove()
    })
    td5.appendChild(b)
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    tr.appendChild(td5)
    pravidla_table.appendChild(tr)
}

function prepsat_shodnost() {
    if (udaj_select.value == "zpráva") {
        je_option.innerText = "je shodná s"
    } else if (udaj_select.value == "číslo protiúčtu") {
        je_option.innerText = "je shodné s"
    }
}

function get_pravidla_from_table() {
    let result = []
    for (let ch of pravidla_table.children) {
        let new_element = {
            "udaj": ch.children[0].innerText,
            "vyskyt": ch.children[1].innerText,
            "klic": ch.children[2].innerText,
            "kategorie": ch.children[3].innerText 
        }
        result.push(new_element)
    }
    return result
}

function vypocist_total(arr) {
    let total = 0
    for (let a of arr) {
        total += a["castka"]
    }
    return total.toFixed(2)
}


function prepocitat() {
    // kouknu, jaky uz jsou kategorie
    let existujici_kategorie = []
    for (let i of roztrizene_platby) {
        if (!existujici_kategorie.includes(i["kategorie"]) && i["kategorie"] != "zbyle") {
            existujici_kategorie.push(i["kategorie"])
        }
    }
    // kouknu, jaky maj existovat a zalozim je
    let jake_maji_existovat = []
    let pravidla = get_pravidla_from_table()
    for (let p of pravidla) {
        if (!jake_maji_existovat.includes(p["kategorie"])) {
            jake_maji_existovat.push(p["kategorie"])
        }
    }
    // zalozeni novych
    for (let k of jake_maji_existovat) {
        if (!existujici_kategorie.includes(k)) {
            roztrizene_platby.push({
                "kategorie": k,
                "platby":[]
            })
        } 
    }

    // zalozeni novych options
    kategorie_select.innerHTML = ""
    let nova_kategorie_opt = document.createElement("option")
    nova_kategorie_opt.value = "nova_kategorie"
    nova_kategorie_opt.innerText = "Nová kategorie"
    kategorie_select.appendChild(nova_kategorie_opt)
    for (let k of jake_maji_existovat) {
        let opt = document.createElement("option")
        opt.innerText = k
        opt.value = k
        kategorie_select.appendChild(opt)
    }
    let e = new Event("change")
    kategorie_select.dispatchEvent(e)

    // roztrizeni zbylych
    let zbyle = roztrizene_platby.find(k => k["kategorie"] === "zbyle");
    let temp_nove_zbyle = []
    for (let platba of zbyle["platby"]) {
        let zarazeno = false
        for (let pravidlo of pravidla) {
            if (pravidlo["vyskyt"] == "obsahuje"){
                if(platba[pravidlo["udaj"]].includes(pravidlo["klic"])){
                    roztrizene_platby.find(k => k["kategorie"] === pravidlo["kategorie"])["platby"].push(platba)
                    zarazeno = true
                    break
                }
            } else if (pravidlo["vyskyt"] == "je") {
                if (platba[pravidlo["udaj"]] == pravidlo["klic"]){
                    roztrizene_platby.find(k => k["kategorie"] === pravidlo["kategorie"])["platby"].push(platba)
                    zarazeno = true
                    break
                }

            }
        }
        if (!zarazeno) {
            temp_nove_zbyle.push(platba)
        }
    }
    zbyle["platby"] = temp_nove_zbyle
    // zobrazeni vysledku pretrideni
    display_zbyle_vydaje(zbyle["platby"])
    result_div.innerHTML = ""

    for (let k of roztrizene_platby) {
        if (k["kategorie"] != "zbyle") {
            novy_div_roztrizenych(k["kategorie"], k["platby"])
        }
    }
}

function novy_div_roztrizenych(kategorie, platby) {
    let div = document.createElement("div") // v tomhle divu je h3, row a tablediv
    result_div.appendChild(div)
    div.classList.add("vydaje-white-div", "border", "border-primary", "rounded", "p-2", "my-2")
    
    let h3 = document.createElement("h3")
    div.appendChild(h3)
    h3.innerText = kategorie
    
    let row = document.createElement("div") // v row je tabulka s detaily a graf
    div.append(row)
    row.classList.add("row")
    let col1 = document.createElement("div")
    row.appendChild(col1)
    col1.classList.add("col-5")
    let col2 = document.createElement("div")
    row.appendChild(col2)
    col2.classList.add("col-7")
    let plot_div = document.createElement("div")
    col2.appendChild(plot_div)
    plot_platby(plot_div, platby)

    let details_table = document.createElement("table")
    col1.appendChild(details_table)
    details_table.classList.add("table", "table-striped", "table-hover")
    let d_tbody = document.createElement("tbody")
    details_table.appendChild(d_tbody)
    let d_tr1 = document.createElement("tr")
    d_tbody.appendChild(d_tr1)
    let d_tr2 = document.createElement("tr")
    d_tbody.appendChild(d_tr2)
    let d_tr3 = document.createElement("tr")
    d_tbody.appendChild(d_tr3)
    let d_tr4 = document.createElement("tr")
    d_tbody.appendChild(d_tr4)

    let total_vydaju = String(platby.length)
    let pct_vydaju = platby.length / vsechny_platby.length * 100
    let total_castka = vypocist_total(platby)
    let pct_castky = parseFloat(total_castka) / parseFloat(celkova_suma) * 100

    let d_th1 = document.createElement("th")
    let d_td1 = document.createElement("td")
    let d_th2 = document.createElement("th")
    let d_td2 = document.createElement("td")
    let d_th3 = document.createElement("th")
    let d_td3 = document.createElement("td")
    let d_th4 = document.createElement("th")
    let d_td4 = document.createElement("td")
    d_th1.innerText = "Výdajů v kategorii"
    d_th2.innerText = "Podíl počtu výdajů"
    d_th3.innerText = "Suma kategorie"
    d_th4.innerHTML = "Podíl celkové částky"
    d_td1.innerText = total_vydaju
    d_td2.innerText = pct_vydaju.toFixed(2).replace(".", ",") + " %"
    d_td3.innerText = total_castka.replace(".", ",") + " Kč"
    d_td4.innerText = pct_castky.toFixed(2).replace(".", ",") + " %"
    d_tr1.appendChild(d_th1)
    d_tr1.appendChild(d_td1)
    d_tr2.appendChild(d_th2)
    d_tr2.appendChild(d_td2)
    d_tr3.appendChild(d_th3)
    d_tr3.appendChild(d_td3)
    d_tr4.appendChild(d_th4)
    d_tr4.appendChild(d_td4)

    
    let table_div = document.createElement("div")
    div.appendChild(table_div)
    table_div.classList.add("table-responsive", "vysledny-div")

    let table = document.createElement("table")
    table.classList.add("table", "table-striped", "table-hover")
    let thead = document.createElement("thead")
    let tbody = document.createElement("tbody")
    let tr = document.createElement("tr")
    let th1 = document.createElement("th")
    let th2 = document.createElement("th")
    let th3 = document.createElement("th")
    let th4 = document.createElement("th")
    th1.innerText = "Datum"
    th2.innerText = "Částka"
    th3.innerText = "Číslo protiúčtu"
    th4.innerText = "Zpráva"
    tr.appendChild(th1)
    tr.appendChild(th2)
    tr.appendChild(th3)
    tr.appendChild(th4)
    thead.appendChild(tr)
    table.appendChild(thead)
    table.appendChild(tbody)
    table_div.appendChild(table)
    for (let p of platby) {
        let tr = document.createElement("tr")
        let td1 = document.createElement("td")
        let td2 = document.createElement("td")
        let td3 = document.createElement("td")
        let td4 = document.createElement("td")
        td1.innerText = p["datum zaúčtování"]
        td2.innerText = p["castka"]
        td3.innerText = p["číslo protiúčtu"]
        td4.innerText = p["zpráva"]
        tr.appendChild(td1)
        tr.appendChild(td2)
        tr.appendChild(td3)
        tr.appendChild(td4)
        tbody.appendChild(tr)
    }
}

function plot_platby(div, platby) {
    let mesice = ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]
    let penize = [0,0,0,0,0,0,0,0,0,0,0,0]
    let min_month = 13
    let max_month = 0
    for (let p of platby) {
        let month = parseInt(p["datum zaúčtování"].split(".")[1])
        if (month < min_month) {
            min_month = month
        } 
        if (month > max_month) {
            max_month = month
        }
        penize[month-1] += p["castka"]
    }

    let plot_div = div

    let data = [{
        x: mesice.slice(min_month-1, max_month),
        y: penize.slice(min_month-1, max_month),
        marker: {
            color: "blue"
        }
    }]

    let layout = {
        yaxis: {
            title: 'Výdaje [Kč]',
            rangemode: "tozero",
            autosize: true
        }
    }

    let config = {
        responsive: true
    }
    Plotly.newPlot(plot_div, data, layout, config)
}

function nakreslit_main_plot(platby) {
    let mesice = ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]
    let penize = [0,0,0,0,0,0,0,0,0,0,0,0]
    let min_month = 13
    let max_month = 0
    for (let p of platby) {
        let month = parseInt(p["datum zaúčtování"].split(".")[1])
        if (month < min_month) {
            min_month = month
        } 
        if (month > max_month) {
            max_month = month
        }
        penize[month-1] += p["castka"]
    }
    
    let data = [{
        x: mesice.slice(min_month-1, max_month),
        y: penize.slice(min_month-1, max_month),
        marker: {
            color: "blue"
        }
    }]

    let layout = {
        yaxis: {
            title: 'Výdaje [Kč]',
            rangemode: "tozero",
            autosize: true
        }
    }

    let config = {
        responsive: true
    }
    Plotly.newPlot(main_plot_div, data, layout, config)
}


csv_file_input.addEventListener('change', function (e) {
    const file = e.target.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {
        const csvData = event.target.result;
        vsechny_platby = csvToObjectArray(csvData);
        roztrizene_platby.push({
            "kategorie": "zbyle",
            "platby": vsechny_platby
        })
        celkova_suma = vypocist_total(vsechny_platby)
        display_zbyle_vydaje(vsechny_platby);
        nakreslit_main_plot(vsechny_platby)
        prepocitat()
    };

    reader.readAsText(file);
});

pravidla_file_input.addEventListener("change", function(e) {
    const file = e.target.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {
        let jsonData = event.target.result;
        let jsonObject = JSON.parse(jsonData);
        for (let obj of jsonObject) {
            display_pravidlo(obj["udaj"], obj["vyskyt"], obj["klic"], obj["kategorie"])
        }
        nahrat_pravidla_div.hidden = "hidden"
        pravidla_div.hidden = ""
    };

    reader.readAsText(file);
})


jsem_tu_nove_button.addEventListener("click", function() {
    pravidla_buttons_div.hidden = "hidden"
    pravidla_div.hidden = ""
})

mam_pravidla_button.addEventListener("click", function() {
    pravidla_buttons_div.hidden = "hidden"
    nahrat_pravidla_div.hidden = ""
})


stahnout_pravidla_button.addEventListener("click", function() {
    result = get_pravidla_from_table()
    let json_string = JSON.stringify(result, null, 4)
    let blob = new Blob([json_string], { type: "application/json" });
    let url = URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "pravidla.json";
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
})

kategorie_select.addEventListener("change", function() {
    if (kategorie_select.value == "nova_kategorie") {
        kategorie_input.hidden = ""
    } else {
        kategorie_input.hidden = "hidden"
    }
})

udaj_select.addEventListener("change", prepsat_shodnost)

nove_pravidlo_button.addEventListener("click", function() {
    let udaj = udaj_select.value
    let vyskyt = vyskyt_select.value
    let klic = klic_input.value
    let kategorie = ""
    if (kategorie_select.value == "nova_kategorie") {
        kategorie = kategorie_input.value
        let opt = document.createElement("option")
        opt.value = kategorie
        opt.innerText = kategorie
        kategorie_select.appendChild(opt)
        kategorie_input.value = null
    } else {
        kategorie = kategorie_select.value
    }
    display_pravidlo(udaj, vyskyt, klic, kategorie)
    prepocitat()
})

prepocitat_button.addEventListener("click", function() {
    prepocitat()
})

datum_sort.addEventListener("click", function() {
    misto_sort_span.innerText = "●"
    castka_sort_span.innerText = "●"
    let zbyle_platby = roztrizene_platby.find(k=> k["kategorie"] === "zbyle")["platby"]
    function datum_creator(datestring) {
        let day = parseInt(datestring.split(".")[0])
        let month = parseInt(datestring.split(".")[1])
        let year = parseInt(datestring.split(".")[2])
        return new Date(year, month, day)
    }
    if (datum_sort_span.innerText == "▼") {
        datum_sort_span.innerText = "▲"
        display_zbyle_vydaje(zbyle_platby.sort(function(a, b) {return datum_creator(a["datum zaúčtování"]) - datum_creator(b["datum zaúčtování"])}))

    } else {
        datum_sort_span.innerText = "▼"
        display_zbyle_vydaje(zbyle_platby.sort(function(a, b) {return datum_creator(b["datum zaúčtování"]) - datum_creator(a["datum zaúčtování"])}))

    }
})

misto_sort.addEventListener("click", function() {
    datum_sort_span.innerText = "●"
    castka_sort_span.innerText = "●"
    let zbyle_platby = roztrizene_platby.find(k=> k["kategorie"] === "zbyle")["platby"] 
    if (misto_sort_span.innerText == "▼") {
        misto_sort_span.innerText = "▲"
        display_zbyle_vydaje(zbyle_platby.sort(function(a, b) {return a["misto"].localeCompare(b["misto"])}))
    } else {
        misto_sort_span.innerText = "▼"
        zbyle_platby.sort(function(a, b) {return b["misto"].localeCompare(a["misto"])})
        display_zbyle_vydaje(zbyle_platby)
    }
})

castka_sort.addEventListener("click", function() {
    misto_sort_span.innerText = "●"
    datum_sort_span.innerText = "●"
    let zbyle_platby = roztrizene_platby.find(k=> k["kategorie"] === "zbyle")["platby"] 
    if (castka_sort_span.innerText == "▼") {
        castka_sort_span.innerText = "▲"
        display_zbyle_vydaje(zbyle_platby.sort(function(a, b) {return a["castka"]-b["castka"]}))
    } else {
        castka_sort_span.innerText = "▼"
        display_zbyle_vydaje(zbyle_platby.sort(function(a, b) {return b["castka"]-a["castka"]}))
    }
})