let active_tab = "#HW";

const $hw_page_button = document.getElementById("HW-page");
const $sw_page_button = document.getElementById("SW-page");
const $skills_page_button = document.getElementById("skills-page");
const $next_question_button = document.querySelectorAll(".next")
const $previous_question_button = document.querySelectorAll(".previous")
const $finish_button = document.getElementById("finish");
const $modal_accept_button = document.getElementById("modal-accept");
const $modal_decline_button = document.getElementById("modal-decline");

const $hw_element = document.querySelectorAll(".hw-element");
const $sw_element = document.querySelectorAll(".sw-element");
const $skills_element = document.querySelectorAll(".skills-element");
const $hw_radio = document.querySelectorAll(".hw-radio");
const $sw_radio = document.querySelectorAll(".sw-radio");
const $skills_radio = document.querySelectorAll(".skills-radio");

let hw_object = {_count: 0,
    _pointer:0,
    _total: $hw_element.length,
    _selected: [],
    _id: "HW"};
let sw_object = {_count: 0,
    _pointer:0,
    _total: $sw_element.length,
    _selected: [],
    _id: "SW"};
let skills_object = {_count: 0,
    _pointer:0,
    _total: $skills_element.length,
    _selected: [],
    _id: "Skills"};

window.addEventListener('load', function () {
    document.getElementById("form-navigation").style.display='inline-block';
    update_question($hw_element[0], false, 'inline-block');
    update_question($sw_element[0], false, 'inline-block');
    update_question($skills_element[0], false, 'inline-block');
    if (sessionStorage.getItem("user") === getCookie("user")){
        const modal = document.getElementById("modal")
        modal.classList.add("show");
        document.body.classList.add("modal-open");
    }
});

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

$hw_page_button.addEventListener("click", function () {
    console.log("HW")
    swap_active_page("#HW");
});

$sw_page_button.addEventListener("click", function () {
    swap_active_page("#SW");
});

$skills_page_button.addEventListener("click", function () {
    swap_active_page("#Skills");
});

window.addEventListener('beforeunload', function(event) {
    if (hw_object._count !== 0 || sw_object._count !== 0 || skills_object._count !== 0) {
        save_form();
    }
});

//Выключает предупреждение при закрытии\перезагрузке страницы если форма пуста
window.addEventListener('onbeforeunload', function (event) {
    if (hw_object._count === 0 && sw_object._count === 0 && skills_object._count === 0) {
        event.preventDefault();
    }
})

$hw_radio.forEach(function(element) {
    element.addEventListener("click", function() {
        console.log("hw clicked")
        update_counter(this, hw_object, $hw_page_button);
        this.closest('div').querySelector('.next').disabled = false
    });
});

$sw_radio.forEach(function(element) {
    element.addEventListener("click", function() {
        update_counter(this, sw_object, $sw_page_button);
        this.closest('div').querySelector('.next').disabled = false
    });
});

$skills_radio.forEach(function(element) {
    element.addEventListener("click", function() {
        update_counter(this, skills_object, $skills_page_button);
        this.closest('div').querySelector('.next').disabled = false
    });
});

function step_forward(element, object){
    update_question(element[object._pointer], true, 'none');
    update_question(element[object._pointer+1], false, 'inline-block');
    element[object._pointer].scrollIntoView();
    object._pointer++;
}
$next_question_button.forEach(function (element) {
    element.addEventListener('click', function (elem) {
        switch (active_tab) {
            case "#HW":
                if (hw_object._pointer !== hw_object._total) {
                    step_forward($hw_element ,hw_object)
                }
                break;

            case "#SW":
                if (sw_object._pointer !== sw_object._total) {
                    step_forward($sw_element ,sw_object)
                }
                break;

            case "#Skills":
                if (skills_object._pointer !== skills_object._total) {
                    step_forward($skills_element, skills_object)
                }
                break;
            default:
                void show_warning(`Ошибка блока управления кнопками перехода. Текущая страница: ${active_tab}`);
                break;
        }
    })
});

function step_back(element, object){
    update_question(element[object._pointer-1], false, 'inline-block');
    update_question(element[object._pointer], true, 'none');
    element[object._pointer-1].scrollIntoView();
    object._pointer--;
}
$previous_question_button.forEach(function (element) {
    element.addEventListener('click', function (elem) {
        switch (active_tab) {
            case "#HW":
                if (hw_object._pointer !== 0) {
                    step_back($hw_element, hw_object);
                }
                break;

            case "#SW":
                if (sw_object._pointer !== 0) {
                    step_back($sw_element, sw_object);
                }
                break;

            case "#Skills":
                if (skills_object._pointer !== 0) {
                    step_back($skills_element, skills_object);
                }
                break;

            default:
                void show_warning(`Ошибка блока управления кнопками перехода. Текущая страница: ${active_tab}`);
                break;
        }
    })
})

$finish_button.addEventListener("click", function() {
    if (hw_object._count === hw_object._total && sw_object._count === sw_object._total && skills_object._count === skills_object._total) {
    //if (true){
        let data = {
            "HW": form_data(document.getElementById(hw_object._id)),
            "SW": form_data(document.getElementById(sw_object._id)),
            "Processes": form_data(document.getElementById(skills_object._id)),
        };

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


/**
 *
 * @param {Element} element
 * @param {string} display
 * @param {boolean} disabled
 */
function update_question(element,disabled, display){
    element.querySelectorAll('input').forEach(function (elem) {
        elem.disabled = disabled;
    })
    element.querySelectorAll('.question-button').forEach(function (elem) {
        elem.style.display = display
    })
}

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
 * Функция для обновления и вывода счетчиков заполненных полей формы конкретного блока
 * @param {HTMLSelectElement}element Элемент блока <select>, на который повешен слушатель onChange
 * @param object объект в котором хранится информация о блоке формы(HW, SW, Skills), в т.ч. и счетчик
 * @param {HTMLButtonElement}button_object Кнопка навигации по форме, в название которой и дописывается значение счетчика. Прим.: HW(10/216)
 */
function update_counter(element, object, button_object) {
    let s = element.name;
    if (object._selected.indexOf(s) === -1) {
        object._selected.push(s);
        object._count++;
        button_object.textContent = `${object._id}(${object._count}/${object._total})`;
    }
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

/**
 * Формирует массив с данными из конкретного блока формы
 * @param {Element}global_element <div> элемент представляющий блок формы(HW, SW, Skills)
 * @returns {[{ _product: "", _selections: [] }]} Массив элементов вида {_product : "", _selections: []},
 * где _product - название продукта, _selections - выбранные пользователем ответы(параметр value:int выбранного варианта)
 */
function form_data(global_element) {
    let arr = [];
    Array.from(global_element.querySelectorAll('.sub-block')).forEach(function(div) {
        let obj = { _product: "", _selections: [] };
        obj._product = div.querySelector('h2').textContent;
        Array.from(div.querySelectorAll('input:checked')).forEach(function(option) {
            obj._selections.push(option.value);
        });
        arr.push(obj);
    });

    return arr;
}

/**
 *
 */
function save_form(){
    let data = {
            "HW": form_data(document.getElementById(hw_object._id)),
            "SW": form_data(document.getElementById(sw_object._id)),
            "Skills": form_data(document.getElementById(skills_object._id)),
    };
    sessionStorage.setItem("formData", JSON.stringify(data));
    sessionStorage.setItem("user", getCookie("user"));
}

//TODO: Сравнить с вариантом через IndexedDB
function load_form() {
    let form = JSON.parse(sessionStorage.getItem("formData"));
    let to_exec_array = []
    console.log(form)
    for (let key in form) {
        if (form.hasOwnProperty(key)) {
            let blocks = document.getElementById(key).querySelectorAll(".sub-block");
            for (let i = 0; i < blocks.length; i++) {
                let elems = blocks[i].querySelectorAll("div")
                let selections = form[key][i]._selections
                for (let j = 0; j < selections.length; j++) {
                    elems[j].querySelectorAll('button').forEach(function (element) {
                        element.disabled = false;
                    })
                    elems[j].querySelectorAll('input').forEach(function (element) {
                        if (element.value == selections[j]){
                            element.checked = true;
                        }
                    })
                    console.log("############")
                }
            }
        }
    }

}


/**
 *
 */
function clear_form() {
    sessionStorage.removeItem("formData");
    sessionStorage.removeItem("user");
}

/**
 *
 */
function close_modal() {
    document.getElementById("modal").classList.remove("show");
    document.body.classList.remove("modal-open");
}

/**
 *
 * @param name
 * @returns {string}
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}