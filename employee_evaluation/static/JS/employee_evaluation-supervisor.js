const $filters = document.getElementById("filters");
const $supervisor_switch = document.getElementById("supervisor-switch");
const $cert__class = document.getElementById("cert--class");
const $cert__subclass = document.getElementById("cert--subclass");


$supervisor_switch.addEventListener("change", ()=>{
    $filters.classList.toggle("expanded");
});

$cert__class.addEventListener("change", ()=>{
    $cert__subclass.querySelectorAll("option").forEach(function (el){
        if (!el.classList.contains($cert__class.value)){
            el.style.display = 'none';
        } else {
             el.style.display = 'block';
        }
    });
    $cert__subclass.querySelector("option.DF").selected = true
});

