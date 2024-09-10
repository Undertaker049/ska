const $links = document.querySelector(".links");
const $expand_links_list_button = document.getElementById("links__expand-button");

const $hw_button = document.getElementById("hw_block");
const $sw_button = document.getElementById("sw_block");
const $pr_button = document.getElementById("pr_block");
const $finish_button = document.querySelector(".button--finish")

const $hw_block = document.getElementById("hw");
const $hw_links = document.getElementById("hw_links")
const $sw_block = document.getElementById("sw");
const $sw_links = document.getElementById("sw_links");
const $pr_block = document.getElementById("pr");
const $pr_links = document.getElementById("pr_links");

const $radio_buttons = document.querySelectorAll(".radio-button");

/**
 * @typedef {Object} AssessmentData
 * @property {Map<String, String>} selections - ответы на опросник
 * @property {number} count - Счетчик пройденных вопросов
 * @property {number} total - Общее количество вопросов
 */
/** @type {AssessmentData} **/
let hw_data = {selections: new Map(), count: 0, total: document.querySelectorAll("#hw .block__sub__task").length}
/** @type {AssessmentData} **/
let sw_data = {selections: new Map(), count: 0, total: document.querySelectorAll("#sw .block__sub__task").length}
/** @type {AssessmentData} **/
let pr_data = {selections: new Map(), count: 0, total: document.querySelectorAll("#pr .block__sub__task").length}

$expand_links_list_button.addEventListener("click", ()=>{
    $links.classList.toggle("links--expanded");
    $links.classList.toggle("links--collapsed");
});

$hw_button.addEventListener("click", ()=>{
    show_block($hw_block, $hw_links, [$sw_block, $pr_block], [$sw_links, $pr_links]);
});

$sw_button.addEventListener("click", ()=>{
    show_block($sw_block, $sw_links, [$hw_block, $pr_block], [$hw_links, $pr_links]);
});

$pr_button.addEventListener("click", ()=>{
    show_block($pr_block, $pr_links, [$hw_block, $sw_block], [$hw_links, $sw_links]);
});

$radio_buttons.forEach((elt) => {
   elt.addEventListener("click", ()=>{
       // Работает конечно, но насколько это корректнее чем evt.target?
       process_click(elt);
   });
});

$finish_button.addEventListener("click", ()=>{
    if (hw_data.count === hw_data.total &&
        sw_data.count === sw_data.total &&
        pr_data.count === pr_data.total) {
        let data = {
            "HW": Array.from(hw_data.selections),
            "SW": Array.from(sw_data.selections),
            "Processes": Array.from(pr_data.selections),
        }
    }
});

window.addEventListener("beforeunload", ()=>{
    save_data_in_browser();
});


/**
 * Behold! Переключатель блоков в самом корявом его исполнении
 * @param active{HTMLDivElement} Активируемый блок
 * @param active_links{HTMLDivElement} Ссылки активируемого блока
 * @param passive{Array} Неактивные блоки
 * @param passive_links{Array} Ссылки неактивных блоков
 */
function show_block(active,active_links, passive, passive_links){
    passive.forEach((elt) => {
        elt.classList.add("hidden");
    })
    passive_links.forEach((elt) => {
        elt.classList.add("hidden");
    })

    active.classList.remove("hidden");
    active_links.classList.remove("hidden");
}


function process_click(radio_elt) {
    let v = radio_elt.value;
    let n = radio_elt.name.replaceAll("_", " ");
    switch(radio_elt.closest(".block").id) {
        case "hw":
            save_choice(n,v,hw_data, "Hardware", $hw_button);
            console.log(Array.from(hw_data.selections))
            break;
        case "sw":
            save_choice(n,v,sw_data, "Software", $sw_button);
            break;
        case "pr":
            save_choice(n,v,pr_data, "Processes", $pr_button);
            break;
    }
    radio_elt.closest(".block__sub__task").classList.add("block__sub__task--checked")
}


/**
 * Функция для записи ответов опросника
 * @param name{String} поле name нажатой radio кнопки
 * @param value{String} выбранный уровень
 * @param block_object{AssessmentData} объект блока для хранения данных
 * @param block_name{String} название блока
 * @param block_button{HTMLButtonElement} кнопка блока(та что для навигации между блоками)
 */
function save_choice(name, value, block_object, block_name, block_button) {
    if (!block_object.selections.has(name)) {
        block_object.selections.set(name,value);
        block_object.count++;
        block_button.textContent = `${block_name}(${block_object.count}/${block_object.total})`;
    }
    else {
        block_object.selections.set(name,value);
    }
}


function save_data_in_browser() {
    localStorage.setItem("SKA_HW", JSON.stringify(Array.from(hw_data.selections)))
    localStorage.setItem("SKA_SW", JSON.stringify(Array.from(sw_data.selections)))
    localStorage.setItem("SKA_PR", JSON.stringify(Array.from(pr_data.selections)))
}