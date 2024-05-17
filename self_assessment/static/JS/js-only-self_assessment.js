let active_tab = "#HW";

const $start_button = document.getElementById("start");
const $hw_page_button = document.getElementById("HW-page");
const $sw_page_button = document.getElementById("SW-page");
const $skills_page_button = document.getElementById("skills-page");
const $finish_button = document.getElementById("finish");
const $modal_accept_button = document.getElementById("modal-accept");
const $modal_decline_button = document.getElementById("modal-decline");

const $hw_element = document.querySelectorAll(".hw-element");
const $sw_element = document.querySelectorAll(".sw-element");
const $skills_element = document.querySelectorAll(".skills-element");

let user_name = "";
let hw_object = {_count: 0,
    _total: $hw_element.length,
    _selected: [],
    _id: "HW"};
let sw_object = {_count: 0,
    _total: $sw_element.length,
    _selected: [],
    _id: "SW"};
let skills_object = {_count: 0,
    _total: $skills_element.length,
    _selected: [],
    _id: "Skills"};

$start_button.addEventListener('click', function() {
    try {
        user_name = document.getElementById("user-name-input").value;
    }catch (e) {
        void show_warning("Сначала введите имя и фамилию!")
    }

    if ((/^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]*$/.test(user_name)) === false) {
        void show_warning("Только Фамилия и Имя, только Кириллица, слова с заглавной буквы");
    } else {
        fetch(`/validate-name?name=${encodeURIComponent(user_name)}`, {
            method: 'GET',
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { void show_warning(text) });
            }else{
                document.getElementById('user-name').style.display = "none";
                document.getElementById("form-navigation").style.display = "inline-block";
                if (localStorage.getItem("name") === user_name){
                    const modal = document.getElementById("modal")
                    modal.classList.add("show");
                    document.body.classList.add("modal-open");
                }
            }
            return response.text();
        })
        .catch(error => {
            void show_warning(error.message);
        });
    }
});

$hw_page_button.addEventListener("click", function () {
    swap_active_page("#HW");
});

$sw_page_button.addEventListener("click", function () {
    swap_active_page("#SW");
});

$skills_page_button.addEventListener("click", function () {
    swap_active_page("#Skills");
});

$hw_element.forEach(function(element) {
    element.addEventListener("change", function() {
        update_counter(this, hw_object, $hw_page_button);
    });
});

$sw_element.forEach(function(element) {
    element.addEventListener("change", function() {
        update_counter(this, sw_object, $sw_page_button);
    });
});

$skills_element.forEach(function(element) {
    element.addEventListener("change", function() {
        update_counter(this, skills_object, $skills_page_button);
    });
});

$finish_button.addEventListener("click", function() {
    if (hw_object._count === hw_object._total && sw_object._count === sw_object._total && skills_object._count === skills_object._total) {
    //if (true){
        let data = {
            "HW": form_data(document.getElementById(hw_object._id)),
            "SW": form_data(document.getElementById(sw_object._id)),
            "Processes": form_data(document.getElementById(skills_object._id)),
            "name": user_name,
        };
        console.log(data);

        fetch('/upload-assessment', {
            method: "POST",
            headers: {
                'Accept': 'application/text',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            body: new URLSearchParams({
                csrfmiddlewaretoken: document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                form: JSON.stringify(data)
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { void show_warning(err.message || "Unknown error") });
            }
            return response.json();
        })
        .catch(err => {
            console.log(err.text);
        });
    } else {
        void show_warning("Сначала заполните форму до конца!");
    }
});

window.addEventListener('beforeunload', function(event) {
    if (hw_object._count !== 0 || sw_object._count !== 0 || skills_object._count !== 0) {
        save_form();
    }
});

//Выключает предупреждение при закрытии\перезагрузке страницы если форма пуста
window.addEventListener('onbeforeunload', function (event) {
    if (hw_object._count === 0 || sw_object._count === 0 || skills_object._count === 0) {
        event.preventDefault();
    }
})

$modal_accept_button.addEventListener("click", function () {
    // let startTime = performance.now()
    load_form();
    // let endTime = performance.now()
    // console.log(`Exec. time ${endTime-startTime} ms`)
    close_modal();
});

$modal_decline_button.addEventListener("click", function () {
    clear_form();
    close_modal();
});

/**
 * Меняет CSS свойство display у указанного блока
 * @param {String}to_page_id ID поле блока, который будет отображен вместо текущего
 */
function swap_active_page(to_page_id) {
    document.querySelector(active_tab).style.display = "none";
    active_tab = to_page_id;
    document.querySelector(to_page_id).style.display = "block";
}

/**
 * Формирует массив с данными из конкретного блока формы
 * @param {Element}global_element <div> элемент представляющий блок формы(HW, SW, Skills)
 * @returns {*[]} Массив элементов вида {_product : "", _selections: []},
 * где _product - название продукта, _selections - выбранные пользователем ответы(параметр value:int выбранного варианта)
 */
function form_data(global_element) {
    let arr = [];
    Array.from(global_element.getElementsByTagName('div')).forEach(function(div) {
        let obj = { _product: "", _selections: [] };
        obj._product = div.id.replace(/_/g, " ");
        Array.from(div.querySelectorAll('p > label > select > option:checked')).forEach(function(option) {
            obj._selections.push(option.value);
        });
        arr.push(obj);
    });

    return arr;
}

/**
 * Функция для обновления и вывода счетчиков заполненных полей формы конкретного блока
 * @param {HTMLSelectElement}element Элемент блока <select>, на который повешен слушатель onChange
 * @param object объект в котором хранится информация о блоке формы(HW, SW, Skills), в т.ч. и счетчик
 * @param {HTMLButtonElement}button_object Кнопка навигации по форме, в название которой и дописывается значение счетчика. Прим.: HW(10/216)
 */
function update_counter(element, object, button_object) {
    let divId = element.closest('div').id;
    let labelFor = element.closest('label').getAttribute('for');
    let s = `${divId}:${labelFor}`;

    if (element.selectedOptions[0].text !== "— Select your level —") {
        if (object._selected.indexOf(s) === -1) {
            object._selected.push(s);
            object._count++;
        }
    } else {
        let index = object._selected.indexOf(s);
        if (index !== -1) {
            object._selected.splice(index, 1);
            object._count--;
        }
    }

    button_object.textContent = `${object._id}(${object._count}/${object._total})`;
}

/**
 * Функция для отображения сообщений об ошибках
 * @param {String}text Текст сообщения
 * @returns {Promise<void>} Возвращаемое значение игнорируется
 */
async function show_warning(text) {
    const errorBox = document.getElementById("error-box");
    errorBox.textContent = text;

    errorBox.style.display = "block";
    errorBox.style.transition = "opacity 0.5s";
    errorBox.style.opacity = '1';

    await new Promise(r => setTimeout(r, 5000));

    errorBox.style.opacity = '0';

    await new Promise(r => setTimeout(r, 500));

    errorBox.style.display = "none";
}

function save_form(){
            let data = {
            "HW": form_data(document.getElementById(hw_object._id)),
            "SW": form_data(document.getElementById(sw_object._id)),
            "Processes": form_data(document.getElementById(skills_object._id))};
        localStorage.setItem("formData", JSON.stringify(data));
        localStorage.setItem("name", user_name);
}

//TODO: Доделать метод восстановления данных из хранилища.
// Сравнить с вариантом через IndexedDB
function load_form() {
    let form = JSON.parse(localStorage.getItem("formData"));
    for (let key in form) {
        if (form.hasOwnProperty(key)) {
            form[key].forEach(element => {
                let product = document.getElementById(`${element._product.replaceAll(" ", "_")}`);
                let tasks = product.querySelectorAll('p > label > select');
                let vals = element._selections;
                for (let i = 0; i < tasks.length; i++) {
                    tasks[i].value = vals[i];
                }
            });
        }
    }
}

function clear_form() {
    localStorage.removeItem("formData");
    localStorage.removeItem("name");
}

function close_modal() {
    document.getElementById("modal").classList.remove("show");
    document.body.classList.remove("modal-open");
}