import TableCreator from "../table_creator.js"

let budiz_button = document.getElementById("budiz")
let file_input = document.getElementById("file")
let parametry_nacteni_button = document.getElementById("parametry_nacteni_button")
let download_button = document.getElementById("download_button")

parametry_nacteni_button.addEventListener("click", function() {
    document.getElementById("parametry_nacteni").hidden = false
})


let barvy = [
    {
        "znamka": 1,
        "barva": "#2cba00"
    },
    {
        "znamka": 2,
        "barva": "#a3ff00"
    },
    {
        "znamka": 3,
        "barva": "#fff400"
    },
    {
        "znamka": 4,
        "barva": "#ffa700"
    },
    {
        "znamka": 5,
        "barva": "#ff0000"
    },
    {
        "znamka": "Ano",
        "barva": "#2cba00"
    },
    {
        "znamka": "Ne",
        "barva": "#ff0000"
    },
    {
        "znamka": "-",
        "barva": "#ffffff"
    }
    
]


budiz_button.addEventListener("click", function() {
    if (file_input.files[0]) {
        let form_data = new FormData()    
        form_data.append("names_col", document.getElementById("names_col").value)
        form_data.append("results_col", document.getElementById("results_col").value)
        form_data.append("name_row", document.getElementById("name_row").value)
        form_data.append("hranice_12", document.getElementById("hranice_12").value)
        form_data.append("hranice_23", document.getElementById("hranice_23").value)
        form_data.append("hranice_34", document.getElementById("hranice_34").value)
        form_data.append("hranice_45", document.getElementById("hranice_45").value)
        form_data.append("file", file_input.files[0])
        form_data.append("styl", document.getElementById("styl").value)

        $.ajax({
            type: "POST",
            url: "/acga_api/vazeny_prumer",
            data : form_data,
            contentType: false,
            processData: false,
            success: function(data) {
                generate(data)
                download_button.hidden = false
            }
        })
    } else {
        alert("Nebyl nahrán žádný soubor.")
    }

})


function generate(data) {
    data = JSON.parse(data)
    document.getElementById("title").innerText = data.title + " | ACGA"
    let vahy = data["vahy"]
    let studenti = data["studenti"]
    
    let header = ["Jméno"]
    vahy.forEach(element => {
        header.push("Váha " + String(element))
    });
    header.push("Průměr pct.")
    header.push("Kolik chybí")
    header.push("Rezerva")
    header.push("Známka")
    header.push("Klasifikace")
    
    let tc = new TableCreator(document.getElementById("parent_div"))
    tc.make_header(header)

    studenti.forEach(s => {
        let row = []
        let colors = [null]
        let tooltips = [null]
        row.push(s["jmeno"])
        vahy.forEach(v => {
            row.push(s["znamky_dict"].find(x => x["vaha"] == v)["znamky"])
            colors.push(null)
            tooltips.push(null)
        })

        row.push(s["prumer_pct"])
        colors.push(null) // průměr
        tooltips.push(s["vypocet"])

        row.push(s["chybi"])
        colors.push(null)
        tooltips.push(null)

        row.push(s["rezerva"])
        colors.push(null)
        tooltips.push(null)
        
        row.push(s["znamka"])
        colors.push(barvy.find(x => x["znamka"] == s["znamka"])["barva"])
        tooltips.push(null)
        
        row.push(s["klasifikovan"])
        colors.push(barvy.find(x => x["znamka"] == s["klasifikovan"])["barva"])
        tooltips.push(null)


        tc.make_row(row, [], colors, tooltips)
    });
    

    let footer_array = ["Průměr"]
    data.prumery_ve_vahach.forEach(element => {footer_array.push(element)})
    footer_array.push(data.prumer_prumeru)
    footer_array.push("-")
    footer_array.push("-")
    footer_array.push(data.prumer_znamka)
    footer_array.push("-")
    tc.make_header(footer_array)


    download_button.addEventListener("click", function() {
        let a = document.createElement("a")
        let file = new Blob([JSON.stringify(data, null, 4)], {type: "text/plain"})
        a.href = URL.createObjectURL(file)
        a.download = "trida.json"
        a.click()
    }) 
}