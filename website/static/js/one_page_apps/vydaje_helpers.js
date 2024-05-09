// Function to convert CSV data to an array of objects
function csvToObjectArray(csv) {
    const lines = csv.split('\n');
    let start_index = 0
    if (lines[0].includes("Pohyby na účtu")) {
        start_index = 2
    }
    const headers = lines[start_index].split(';');
    const result = [];

    for (let i = start_index+1; i < lines.length; i++) {
        const obj = {};
        const currentLine = lines[i].split(';');
        
        if (currentLine[0] == "") {  // ochrana proti tomu poslednimu prazdnymu
            continue
        }

        for (let j = 0; j < headers.length; j++) {
            if (headers[j] == "částka") {
                obj["castka"] = -parseFloat(currentLine[j].replace(",","."))
            } else if (headers[j] == "zpráva") {
                let misto = currentLine[j].split("Místo: ")[1]
                if (misto) {
                    obj["misto"] = currentLine[j].split("Místo: ")[1]
                } else {
                    obj["misto"] = ""
                }
                obj["zpráva"] = currentLine[j]
            } else {
                obj[headers[j]] = currentLine[j];
            }
        }

        result.push(obj);   
    }
    return result;
}


export default csvToObjectArray