const $hw_page_button = document.getElementById('hw-page');
const $sw_page_button = document.getElementById('sw-page');
const $pr_page_button = document.getElementById('processes-page');
const $finish_button = document.getElementById('finish');
const $back_button = document.getElementById('back');
const $modal_accept_button = document.getElementById("modal-accept");
const $modal_decline_button = document.getElementById("modal-decline");

window.addEventListener('load', function () {
    fetch('/self-assessment/validate-name').then(response => {
        if (!response.ok) {
            $finish_button.disabled = true;
            return response.text().then(text => {showSnackbar(text)});
        } else {
            if (localStorage.getItem("formData") !== null) {
                document.getElementById("modal").classList.add("show");
                document.body.classList.add("modal-open");
            }
        }
    });
});

$hw_page_button.addEventListener('click', function (){
    hide_form_elements();
    document.getElementById("HW").style.display = 'block';
});

$sw_page_button.addEventListener('click', function () {
    hide_form_elements();
    document.getElementById('SW').style.display = 'block';
})

$pr_page_button.addEventListener('click', function (){
    hide_form_elements();
    document.getElementById("Processes").style.display = 'block';
});

$back_button.addEventListener('click', function () {
    window.scrollTo(0,0)
})

$finish_button.addEventListener("click", function() {
    if (hw_page_object._count === hw_page_object._total && sw_page_object._count === sw_page_object._total && pr_page_object._count === pr_page_object._total) {
        let data = {
            "HW": form_data(document.getElementById('HW')),
            "SW": form_data(document.getElementById('SW')),
            "Processes": form_data(document.getElementById('Processes')),
        };

        fetch('self-assessment/upload', {
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
                return response.json().then(err => { showSnackbar(err.message || "Unknown error") });
            }
            return response.json();
        })
        .catch(err => {
            console.log(err.text);
        });
    } else {
        showSnackbar("Сначала заполните форму!");
    }
});

window.addEventListener('beforeunload', function() {
    if (hw_page_object._count !== 0 || sw_page_object._count !== 0 || pr_page_object._count !== 0) {
        save_form();
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
    localStorage.removeItem("formData");
    close_modal();
});

/**
 * Формирует данные блока формы для отправки
 * @param {HTMLDivElement}element блок формы (HW/SW/PR)
 * @return {Array[{_product: _selections[{Number}]}]}arr массив объектов вида подблок:массив параметров(value)
 */
function form_data(element){
    let arr = [];
    element.querySelectorAll('.sub-block').forEach(function (e) {
        let obj = { _product: e.querySelector('h2').textContent, _selections: [] };
        e.querySelectorAll('.radio-button').forEach(function (input) {
            if (input.checked === true){
                obj._selections.push(input.value);
            }
        });
        arr.push(obj);
    });
    return arr;
}

function hide_form_elements() {
    document.querySelectorAll('.form-element').forEach(function (e) {
        e.style.display = 'none';
    });
}

function save_form(){
    let data = {};
    document.querySelectorAll('input[type="radio"]:checked').forEach(function (e) {
        data[e.name] = e.value;
    });
    localStorage.setItem("formData", JSON.stringify(data));
}

function load_form() {
    let form = JSON.parse(localStorage.getItem("formData"));
    let keys = Object.keys(form);
    for (let i = 0; i < keys.length; i++) {
        document.querySelectorAll(`input[name="${keys[i]}"]`).forEach(function (e) {
            if (e.value === form[keys[i]]) {
                e.checked = true;
                // Асинхронная функция решает проблемы с блокировкой связанной с вызовом eventListener'ов, как я понял.
                // Да это самый простой способ и восстановить счетчики и снять флажки. Нет не стыдно.
                void emulateClick(e);
            }
        });
    }
}

async function emulateClick(e){
     e.click();
}

function close_modal() {
    document.getElementById("modal").classList.remove("show");
    document.body.classList.remove("modal-open");
}