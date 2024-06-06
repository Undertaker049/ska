/**
 * Автоматическое перемещение до следующего блока вопросов
 * @param {string}parent_id ID блока формы (HW, SW etc.)
 * @param {number}shift На сколько блоков сместится вперед(+1) или назад(-1)
 * @param page_blocks
 */
function move_to_another_block(parent_id, shift, page_blocks) {
    let keys = Object.keys(page_blocks);
    let index = keys.indexOf(parent_id);
    if (index+shift >= 0 && index+shift <= keys.length) {
        Object.values(page_blocks)[index + shift].scrollIntoView();
    }
    else if(index+shift < 0){
        document.querySelector('header').scrollIntoView();
    }
}

/**
 * Функция для отображения счетчика пройденных вопросов блока формы в тексте кнопки перехода к блоку.
 * @param {string}button_id ID элемента button
 * @param {{_count: number, _total: number}}page_object объект в котором хранятся счетчики страниц
 * @param {string}name Исходный текст кнопки
 */
function update_button_counter(button_id, page_object, name) {
    document.getElementById(button_id).textContent = `${name} (${page_object._count}/${page_object._total})`;
}

/**
 * Функция для отображения сообщений об ошибках
 * @param {String}text Текст сообщения
 * @returns {Promise<void>}
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