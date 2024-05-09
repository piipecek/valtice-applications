const addNoteButton = document.getElementById('new_tone');
const containerDiv = document.getElementById('container');
const enable_sound_btn = document.getElementById("enable")
let counter = 0;

enable_sound_btn.addEventListener("click", () => {
    if (Tone.context.state != "running") {
        Tone.start();
    }
})

addNoteButton.addEventListener('click', () => {
    counter++;
    let synth = new Tone.Synth().toDestination()
    let divId = `noteDiv${counter}`;
    let newDiv = document.createElement('div');
    newDiv.id = divId;
    newDiv.classList.add("border", "border-primary", "rounded-2", "p-2", "m-2", "row")
    // frekvence input a col
    let frekvence_col = document.createElement("div")
    frekvence_col.classList.add("col-4")
    newDiv.appendChild(frekvence_col)
    let frekvence_input = document.createElement("input")
    frekvence_input.classList.add("form-control")
    frekvence_input.type = "number"
    frekvence_input.placeholder = "Zadej frekvenci"
    frekvence_col.appendChild(frekvence_input)

    // spacer col
    let spacer_col = document.createElement("div")
    spacer_col.classList.add("col")
    newDiv.appendChild(spacer_col)

    // play for one second button a col
    let play_1_sec_col = document.createElement("div")
    play_1_sec_col.classList.add("col-auto")
    newDiv.appendChild(play_1_sec_col)
    let play_1_sec_btn = document.createElement("button")
    play_1_sec_btn.classList.add("btn", "btn-outline-primary")
    play_1_sec_btn.innerText = "Play (1 sec)"
    play_1_sec_col.appendChild(play_1_sec_btn)

    play_1_sec_btn.addEventListener("click", () => {
        let f = 440
        if (frekvence_input.value) {
            f = frekvence_input.value
        }
        synth.triggerAttackRelease(f, 1)
    })

    // play inf button a col
    let play_infinitely_col = document.createElement("div")
    play_infinitely_col.classList.add("col-auto")
    newDiv.appendChild(play_infinitely_col)
    let play_infinitely_btn = document.createElement("button")
    play_infinitely_btn.classList.add("btn", "btn-outline-primary")
    play_infinitely_btn.innerText = "Play"
    play_infinitely_col.appendChild(play_infinitely_btn)

    play_infinitely_btn.addEventListener("click", () => {
        if (play_infinitely_btn.innerText == "Play") {
            console.log("playing")
            play_infinitely_btn.innerText = "Stop"
            let f = 440
            if (frekvence_input.value) {
                f = frekvence_input.value
            }
            synth.triggerAttack(f, 1)
        } else {
            console.log("stopping")
            play_infinitely_btn.innerText = "Play"
            synth.triggerRelease()
        }
    })
    
    // smazat button a col
    let smazat_col = document.createElement("div")
    smazat_col.classList.add("col-auto")
    newDiv.appendChild(smazat_col)
    let smazat_btn = document.createElement("button")
    smazat_btn.innerText = "Smazat tón"
    smazat_btn.addEventListener("click", () => {
        synth.triggerRelease()
        newDiv.remove()
    })
    smazat_btn.classList.add("btn", "btn-outline-danger")
    containerDiv.appendChild(newDiv)
    smazat_col.appendChild(smazat_btn)
})