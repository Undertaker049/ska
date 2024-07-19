const $filters = document.getElementById("filters");
const $supervisor_switch = document.getElementById("supervisor-switch");
const $cert__class = document.getElementById("class");
const $cert__subclass = document.getElementById("sub-class");

const $task_select = document.querySelectorAll(".task")
const $add_filter_button =document.querySelectorAll(".add-filter")

let subordinates = []
let filters = []
let filterIDCounter = -1

fetch("/employee-evaluation/subordinates", {method: "GET"}).then(resp =>{
    if (resp.ok){
        resp.text().then(data=>{
            subordinates = JSON.parse(data).data;
        });
    }
});

$supervisor_switch.addEventListener("change", ()=>{
    $filters.classList.toggle("expanded");
});

$task_select.forEach(function (el) {
    el.addEventListener("change", function (evt){
        let node = evt.target
        if (node.value !== "Total"){
            node.parentNode.querySelector(".filter_value").style.display = 'none'
            node.parentNode.querySelector(".level").style.display = 'inline-block'
        }
        else {
            node.parentNode.querySelector(".filter_value").style.display = 'inline-block'
            node.parentNode.querySelector(".level").style.display = 'none'
        }
    })
});

$add_filter_button.forEach(function (el) {
    el.addEventListener("click", ()=> {
        let node = el.parentNode;
        let filter = {};
        switch (node.id) {
            case "hw":
            case "sw":
                if (node.querySelector(".filter_value").value === ''){
                    showSnackbar("Введите значение для фильтра!");
                    return;
                }

                filter = {"block": node.id,
                    "product": node.querySelector(".product").value,
                    "task": node.querySelector(".task").value,
                    "sign": node.querySelector(".sign").value,
                    "id":getID()};
                if (filter["task"] === "Total") {
                    filter["value"] = node.querySelector(".filter_value").value;

                } else {
                    filter["value"] = node.querySelector(".level").value;
                }
                filters.push(filter);
                break;
            case "pr":
                filter = {"block": "pr",
                    "product": node.querySelector(".product").value,
                    "sign": node.querySelector(".sign").value,
                    "value": node.querySelector(".level").value,
                    "id":getID()};
                break;
            case "cr":
                if (node.querySelector("#class").value === "------"){
                    showSnackbar("Укажите класс сертификата!")
                    return;
                }
                filter = {"block": "cr",
                    "class": $cert__class.value,
                    "subclass": $cert__subclass.value,
                    "id":getID()};
                break;
            default:
                showSnackbar("Не понятно, из какого блока фильтр!");
                return;
        }
        node.querySelector(".filters").innerHTML +=
            `<span class="filter" data-id="${filter["id"]}">` +
            filterToString(filter) +
            `<button class="delete-filter" onclick="` +
            `removeFromFiltersList(this.dataset.id);`+
            `this.parentNode.remove();` +
            `">x</button>` +
            `</span>`;
})
});

$cert__class.addEventListener("change", ()=>{
    $cert__subclass.querySelectorAll("option").forEach(function (el){
        if (!el.classList.contains($cert__class.value)){
            el.style.display = 'none';
        } else {
            el.style.display = 'block';
        }
    });
    $cert__subclass.querySelector("option.DF").selected = true;

});

function filterToString(filter){
    switch (filter["block"]) {
        case "hw":
        case "sw":
            return `${filter["product"]}: ${filter["task"]} ${filter["sign"]} ${filter["value"]}`;
        case "pr":
            return `${filter["product"]} ${filter["sign"]} ${filter["value"]}`;
        case "cr":
            return `${filter["class"]}: ${filter["subclass"]}`;
        default:
            return "unknown filter";
    }
}

function removeFromFiltersList(id) {
    for (let i = 0; i < filters.length; i++) {
        if (Number(filters[i]["id"]) === Number(id)){
            filters.splice(i, 1)
            break
        }
    }
}

function getID() {
    filterIDCounter++
    return filterIDCounter;
}

