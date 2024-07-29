const $filters = document.getElementById("filters");
const $supervisor_switch = document.getElementById("supervisor-switch");
const $cert__class = document.getElementById("class");
const $cert__subclass = document.getElementById("sub-class");

const $task_select = document.querySelectorAll(".task")
const $add_filter_button = document.querySelectorAll(".add-filter")
const $employees = document.querySelectorAll(".employee");

const $table = document.getElementById("employees-table")

let subordinates = [];
let filters = {};
let filterIDCounter = -1;

/**
 * Превентивный запрос списка подчиненных
 */
document.addEventListener("DOMContentLoaded", ()=>{
    fetch("/employee-evaluation/subordinates", {method: "GET"}).then(resp =>{
        if (resp.ok){
            resp.text().then(data=>{
                subordinates = JSON.parse(data).data
                    $employees.forEach(function (el) {
                        if (subordinates.indexOf(Number(el.querySelector("td").textContent)) !== -1){
                            el.classList.toggle("subordinate");
                        }
                    });
            });
        }
    });
});

/**
 * Раскрытие/закрытие блока с фильтрами
 * В этом режиме в списке сотрудников остаются только прямые подчиненные
 */
$supervisor_switch.addEventListener("click", (ev)=>{
    if (ev.target.checked) {
        $filters.classList.toggle("expanded");
        $employees.forEach(function (el) {
            if (!el.classList.contains("subordinate")) {
                el.style.display = "none"
            }
        });
    } else {
        $filters.classList.toggle("expanded");
        disableSupervisor()
    }
});

/**
 * Метод, меняющий поля фильтра в зависимости от того, по какому значению ставится фильтр:
 * Total - суммарный счет по дисциплине - числовой
 * Дисциплина - уровень - выбор уровня
 */
$task_select.forEach(function (el) {
    el.addEventListener("click", function (evt){
        let node = evt.target;
        if (node.value !== "Total"){
            node.parentNode.querySelector(".filter_value").style.display = 'none';
            node.parentNode.querySelector(".level").style.display = 'inline-block';
        }
        else {
            node.parentNode.querySelector(".filter_value").style.display = 'inline-block';
            node.parentNode.querySelector(".level").style.display = 'none';
        }
    });
});

/**
 * Добавление фильтра, в зависимости от блока, к которому он добавляется, зависит его формат
 */
$add_filter_button.forEach(function (el) {
    el.addEventListener("click", ()=> {
        let node = el.parentNode;
        let filter = {};
        switch (node.id) {
            case "hw":
            case "sw":
                filter = {
                    "id":getID(),
                    "block": node.id,
                    "product": node.querySelector(".product").value,
                    "task": node.querySelector(".task").value,
                    "sign": node.querySelector(".sign").value
                };

                if (filter["task"] === "Total") {
                    filter["value"] = node.querySelector(".filter_value").value;
                    if (filter["value"] === ""){
                        showSnackbar("Введите значение для фильтра!");
                        return;
                    }
                } else {
                    filter["value"] = node.querySelector(".level").value;
                }
                break;
            case "pr":
                filter = {
                    "id":getID(),
                    "block": "pr",
                    "process": node.querySelector(".process").value,
                    "sign": node.querySelector(".sign").value,
                    "value": node.querySelector(".level").value,
                    };
                break;
            case "cr":
                if (node.querySelector("#class").value === "any"){
                    showSnackbar("Укажите класс сертификата!")
                    return;
                }
                filter = {
                    "id":getID(),
                    "block": "cr",
                    "category": $cert__class.value,
                    "subcategory": $cert__subclass.value};
                break;
            default:
                showSnackbar(`Не понятно, из какого блока фильтр ${node.id}!`);
                return;
        }
        filters[filter.id] = filter;
        node.querySelector(".filters").innerHTML +=
            `<span class="filter" data-id="${filter["id"]}">` +
            `<span class="filter--data">${filterToString(filter)}</span>` +
            `<button class="delete-filter" onclick="` +
            `delete filters[this.parentNode.dataset.id];`+
            `this.parentNode.remove();` +
            `">x</button>` +
            `</span>`;
    });
});

/**
 * Изменение отображаемых подклассов сертификатов, в зависимости от класса
 */
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

/**
 * Строковое представление фильтра для его отображения в добавленные
 * @param filter объект фильтра
 * @return {string} строковое представление фильтра
 */
function filterToString(filter){
    switch (filter["block"]) {
        case "hw":
        case "sw":
            return `${filter["product"]}: ${filter["task"]} ${filter["sign"]} ${filter["value"]}`;
        case "pr":
            return `${filter["product"]} ${filter["sign"]} ${filter["value"]}`;
        case "cr":
            return `${filter["category"]}: ${filter["subcategory"]}`;
        default:
            return "unknown filter";
    }
}

/**
 * Простенький генератор для создания id фильтров, чтобы их было проще удалять
 * @return {number}
 */
function getID() {
    filterIDCounter++
    return filterIDCounter;
}

/**
 * Очищает массив фильтров, удаляет сами фильтры, возвращает видимость всех сотрудников при выходе из "режима начальника",
 */
function disableSupervisor(){
    document.querySelectorAll(".filters").forEach((el)=>{
        el.innerHTML = "";
    });
    filters = [];
    $employees.forEach(function (el) {
        el.style.display = "table-row";
    });
}

/**
 * Отправляет список фильтров и id сотрудников для фильтрации на сервер
 */
function sendFilters() {
    console.log()
    if (Object.keys(filters).length === 0) {
        showSnackbar("Сначала добавьте фильтры!")
        return
    }

    fetch("/employee-evaluation/subordinates/filter", {
        method: "POST",
        headers:{"X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value},
        body: new URLSearchParams({"data": JSON.stringify({subordinates: subordinates, filters: filters})}),
    }).then(resp => {
       if (resp.ok) {
           resp.text().then(msg => {

               /**
                * @type {{data: Array, data_for_table: Array, headers_for_table: Array}}
                */
               let d = JSON.parse(msg)
               let matches = d.data;
               let data_for_table = d.data_for_table;

               let thead = $table.querySelector("thead")
               let tr_tbody = $table.querySelectorAll("tbody > tr")


               console.log(data_for_table[Object.keys(data_for_table)[0]][0])
               console.log(d.headers_for_table)


               document.querySelectorAll(".subordinate").forEach(el =>{
                   if (matches.indexOf(Number(el.querySelector("td").textContent)) === -1) {
                       el.style.display = 'none';
                   } else {
                       el.style.display = 'table-row';
                   }

               });
               // for (const id in JSON.parse(msg).data) {
               //
               // }
           });
       } else if (resp.status === 404) {
           resp.text().then(e =>{
               showSnackbar("После отмеченного фильтра осталось 0 сущностей для фильтрации!");
               document.querySelector(`.filter[data-id="${e}"]`).classList.add("failing-filter");
           });
       }
    });
}

function appendToTable(data) {

}

/**
 * Позволяет сохранить таблицу с отобранными сотрудниками в csv формате
 */
function saveCSV() {

}