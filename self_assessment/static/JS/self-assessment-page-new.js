// TODO удалить все остальные .js файлы в директории, они не используются
const $links = document.querySelector(".links");
const $expand_links_list_button = document.getElementById("links__expand-button");

const $hw_button = document.getElementById("hw_block");
const $sw_button = document.getElementById("sw_block");
const $pr_button = document.getElementById("pr_block");
const $finish_button = document.querySelector(".button--finish");

const $hw_block = document.getElementById("hw");
const $hw_links = document.getElementById("hw_links")
const $sw_block = document.getElementById("sw");
const $sw_links = document.getElementById("sw_links");
const $pr_block = document.getElementById("pr");
const $pr_links = document.getElementById("pr_links");

const $modal = document.getElementById("modal");
const $modal_accept = document.getElementById("modal__accept");
const $modal_decline = document.getElementById("modal__decline");

const $radio_buttons = document.querySelectorAll(".radio-button");

/**
 * @typedef {Object} AssessmentData
 * @property {Map<String, String>} selections - ответы на опросник(в json сохраняется как массив [[k, v], [k, v]...])
 * @property {number} count - Счетчик пройденных вопросов
 * @property {number} total - Общее количество вопросов
 */
/** @type {AssessmentData} **/
let hw_data = {selections: new Map(), count: 0, total: document.querySelectorAll("#hw .block__sub__task").length}
/** @type {AssessmentData} **/
let sw_data = {selections: new Map(), count: 0, total: document.querySelectorAll("#sw .block__sub__task").length}
/** @type {AssessmentData} **/
let pr_data = {selections: new Map(), count: 0, total: document.querySelectorAll("#pr .block__sub__task").length}

window.addEventListener('load', function () {
    // TODO убрать срезку с простым toggle_modal()
    fetch('/self-assessment/validate-name', {method: "GET"}).then(response => {
        if (!response.ok) {
            $finish_button.disabled = true;
            return response.text().then(text => {showSnackbar(text)});
        } else {
            toggle_modal();
        }
    });
    // toggle_modal()
});

$modal_accept.addEventListener("click", ()=>{
    toggle_modal();
    load_data_from_browser();
    // Вынести в отдельный метод? Используется то оно только здесь
    let restore = (q, data, block) => {
        if (data.selections.size === 0) {
            return;
        }
        console.log(data.selections)
         for (let i = 0; i < q.length; i++) {
             let button = q[i];
             let name = button.name.replaceAll("_", " ");
             if (data.selections.has(name)){
                 let b =document.querySelector(`${block} input[type="radio"][name="${button.name}"][value="${data.selections.get(name)}"]`);
                 b.checked = true;
                 b.selected = true;
                 b.closest(".block__sub__task").classList.add("block__sub__task--checked");
             }
        }
    }

    restore(document.querySelectorAll("#hw .radio-button"), hw_data, "#hw");
    restore(document.querySelectorAll("#sw .radio-button"), sw_data, "#sw");
    restore(document.querySelectorAll("#pr .radio-button"), pr_data, "#pr");
});

$modal_decline.addEventListener("click", ()=>{
    toggle_modal();
    localStorage.removeItem("SKA_DATA");
});

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
// TODO Убрать срезку с if(true)
    // if(true){
        let d = JSON.stringify({
                        "HW": Array.from(hw_data.selections),
                        "SW": Array.from(sw_data.selections),
                        "Processes": Array.from(pr_data.selections),
                })
        fetch('/self-assessment/upload', {
            method: "POST",
            headers: {
                'Accept': 'application/text',
                // 'Content-Type': '???/??? charset=UTF-8',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: new URLSearchParams({
                data: d
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { showSnackbar(err.message || "Unknown error") });
            }
            else {
                showSnackbar("Результаты записаны!")
                $finish_button.disabled = true
            }
        })
    } else {
        showSnackbar("Сначала выберите ответ во всех вопросах!")
    }
});

window.addEventListener("beforeunload", ()=>{
    save_data_in_browser();
});

function toggle_modal() {
    $modal.classList.toggle("show");
    document.body.classList.toggle("modal-open");
}


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

/**
 * Функция сохраняет выбор по конкретному вопросу формы
 * @param radio_elt{HTMLButtonElement}
 */
function process_click(radio_elt) {
    let v = radio_elt.value;
    let n = radio_elt.name.replaceAll("_", " ");
    switch(radio_elt.closest(".block").id) {
        case "hw":
            save_choice(n,v,hw_data, "Hardware", $hw_button);
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


/**
 * Сохраняет данные в LocalStorage
 */
function save_data_in_browser() {
    localStorage.setItem("SKA_DATA",
        JSON.stringify(
            {
                hw: JSON.stringify(Array.from(hw_data.selections)),
                sw: JSON.stringify(Array.from(sw_data.selections)),
                pr: JSON.stringify(Array.from(pr_data.selections))
            }
        )
    );
}

/**
 * Загружает данные из LocalStorage
 */
function load_data_from_browser() {
    let data = localStorage.getItem("SKA_DATA");
    if (data != null) {
        data = JSON.parse(data);
        hw_data.selections = new Map(JSON.parse(data.hw));
        hw_data.count = hw_data.selections.size
        sw_data.selections = new Map(JSON.parse(data.sw));
        sw_data.count = sw_data.selections.size
        pr_data.selections = new Map(JSON.parse(data.pr));
        pr_data.count = pr_data.selections.size
    }

}