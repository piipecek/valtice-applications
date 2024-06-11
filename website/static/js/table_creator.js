class TableCreator {
    constructor(parentDiv, small = false) {
        this.parentDiv = parentDiv;
        this.parentDiv.innerHTML = ""
        this.table = document.createElement('table')

        let table_responsive_div = document.createElement("div")
        table_responsive_div.classList.add("table-responsive")
        this.table.classList.add("table", "table-hover")
        if (small) {
            this.table.classList.add("table-sm")
        }
        
        this.parentDiv.appendChild(table_responsive_div)
        table_responsive_div.appendChild(this.table)
        
        this.tbody = null
    }

    make_tbody() {
        this.tbody = document.createElement('tbody')
        this.table.appendChild(this.tbody);
    }

    make_header(headerData) {
        const thead = document.createElement('thead');
        const tr = document.createElement('tr');

        headerData.forEach(function (data) {
            const th = document.createElement('th');
            th.textContent = data;
            tr.appendChild(th);
        });

        thead.appendChild(tr);
        this.table.appendChild(thead);
    }

    make_row(rowData, th_indexes = [], colors = [], tooltips = []) {
        if (!this.tbody) {
            this.make_tbody()
        }

        // header_indexes je třeba [1, 0, 1, 0, 0]. Znamená to, kdy použít th a kdy td
        if (th_indexes.length == 0) {
            rowData.forEach(element => {
                th_indexes.push(0)
            });
            th_indexes[0] = 1
        }
        if (colors.length == 0) {
            rowData.forEach(element => {
                colors.push(null)
            });
        }
        if (tooltips.length == 0) {
            rowData.forEach(element => {
                tooltips.push(null)
            });
        }


        const tr = document.createElement('tr');

        for (let i=0;i<th_indexes.length; i++) {
            let is_th = th_indexes[i]
            let data = rowData[i]
            let color = colors[i]
            let tooltip = tooltips[i]
            let col

            if (is_th == 1) {
                col = document.createElement('th');
            } else {
                col = document.createElement('td');
            }

            if (color) {
                col.style.backgroundColor = color
            }
            
            if (typeof data == "string" || typeof data == "number") {
                col.innerText = data
            }

            if (data == null) {
                
            } else if (typeof data == "object") {
                col.appendChild(data)
            }
            
            if (tooltip) {
                col.classList.add("tooltip1")
                let span = document.createElement("span")
                span.classList.add("tooltiptext1", "px-2")
                span.innerHTML = tooltip
                col.appendChild(span)
                MathJax.typeset([span])
            }
            tr.appendChild(col)

        }
        this.tbody.appendChild(tr);
    }
}

export default TableCreator