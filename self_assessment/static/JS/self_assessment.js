let active_tab = "#HW";

let $hw_element = $(".hw-element");
let $sw_element = $(".sw-element");
let $skills_element = $(".skills-element");

let $error_box = $("#error-box");
let $name_input = $("#user-name-input")

let $start_button = $("#start");
let $hw_page_button = $("#HW-page");
let $sw_page_button = $("#SW-page");
let $skills_page_button = $("#skills-page");
let $finish_button = $("#finish");

let user_name = "";
let hw_object = {_count: 0, _total: $hw_element.toArray().length, _selected: [], _id: "HW"};
let sw_object = {_count: 0, _total: $sw_element.toArray().length, _selected: [], _id: "SW"};
let skills_object = {_count: 0, _total: $skills_element.toArray().length, _selected: [], _id: "Skills"};



$start_button.on('click',function() {
    // Для тестов формы раскомментить это
        if (RegExp("^[А-ЯЁ][а-яё]+\\s[А-ЯЁ][а-яё]*").exec($name_input.val()) === null){
            void show_warning("Только Фамилия и Имя, только Кириллица, слова с заглавной буквы");
        }
        else {
            user_name = $name_input.val();
             $.ajax({
                url: '/validate-name',
                type: 'GET',
                 //Выяснить почему работает только так
                data: "name="+user_name,
                success(msg){
                    console.log(msg)
                    $('#user-name').css("display", "none");
                    $("#form-navigation").css("display", "inline-block");
                },
                error(response){
                    void show_warning(response.responseText)
                }
            });
        }
    //Для тестов с отправкой данных раскомментить это
    // user_name = $name_input.val();
    // $('#user_name').css("display", "none");
    // $("#form-navigation").css("display", "inline-block");
});

/**
 * На enter происходит отправка формы через дефолтный метод
 * чтобы этого не происходило, создана данная функция, переопределяющая поведение
 */
$(window).keydown(function(event){
    if(event.keyCode === 13) {
        $start_button.click()
    }
  });

$hw_page_button.on("click", function () {
    swap_active_page("#HW");
});
$sw_page_button.on("click", function () {
    swap_active_page("#SW");
});
$skills_page_button.on("click", function () {
    swap_active_page("#Skills");
});

$hw_element.on("change", function () {
    update_counter(this, hw_object, $hw_page_button);
})

$sw_element.on("change", function () {
    update_counter(this, sw_object, $sw_page_button);
})

$skills_element.on("change", function () {
    update_counter(this, skills_object, $skills_page_button);
})

$finish_button.on("click", function () {
    if (hw_object._count === hw_object._total && sw_object._count === sw_object._total && skills_object._count === skills_object._total){
    // if (true){
        let data = {"HW": form_data($("#"+hw_object._id)),
            "SW": form_data($("#"+sw_object._id)),
            "Processes": form_data($("#"+skills_object._id)),
            "name": user_name,
            }
            console.log(data)

         $.ajax({
        url: '/upload-assessment',
        type: "POST",
        headers: {
            'Accept': 'application/text',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        },
        data: {csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(), form: JSON.stringify(data)},
        dataType: "json",
        success(msg){

        },
        error(msg){
            void show_warning(msg);
        }
    });
    }
    else{
        void show_warning("Сначала заполните форму до конца!");
    }
})

/**
 * Меняет CSS свойство display у указанного блока
 * @param to_page_id ID поле блока, который будет отображен вместо текущего
 */
function swap_active_page(to_page_id) {
    $(active_tab).css("display", "none");
    active_tab = to_page_id;
    $(to_page_id).css("display", "block");
}

/**
 * Формирует массив с данными из конкретного блока формы
 * @param jq_global_element <div> элемент представляющий блок формы(HW, SW, Skills)
 * @returns {*[]} Массив элементов вида {_product : "", _selections: []},
 * где _product - название продукта, _selections - выбранные пользователем ответы(параметр value:int выбранного варианта)
 */
function form_data(jq_global_element) {
    let arr = [];
    jq_global_element.children('div').each(function () {
            let obj = {_product : "", _selections: []}
            obj._product = $(this).attr('id').replaceAll("_", " ");
            $(this).find('> p > label > select option:selected').each(function () {
                obj._selections.push($(this).attr('value'));
            })
        arr.push(obj);
        })

    return arr;
}

/**
 * Функция для обновления и вывода счетчиков заполненных полей формы конкретного блока
 * @param element Элемент блока <select>, на который повешен слушатель onChange
 * @param object объект в котором хранится информация о блоке формы(HW, SW, Skills), в т.ч. и счетчик
 * @param button_object Кнопка навигации по форме, в название которой и дописывается значение счетчика. Прим.: HW(10/216)
 */
function update_counter(element, object, button_object){
    let s = `${$(element).closest('div').attr('id')}:${$(element).closest('label').attr('for')}`;
    if ($(element).find(":selected").text() !== "— Select your level —"){
        if (object._selected.indexOf(s) === -1) {
            object._selected.push(s);
            object._count++;
        }
    } else {
        object._selected.splice(object._selected.indexOf(s),1)
        object._count--;
    }
    button_object.text(`${object._id}(${object._count}/${object._total})`);
}

/**
 * Функция для отображения сообщений об ошибках
 * @param {String}text Текст сообщения
 * @returns {Promise<void>} Возвращаемое значение игнорируется
 */
async function show_warning(text) {
    $error_box.text(text);
    $error_box.fadeTo("slow", 1);
    await new Promise(r => setTimeout(r, 5000));
    $error_box.fadeTo("slow", 0);
    await new Promise(r => setTimeout(r, 500));
    $error_box.css("display", "none");
}