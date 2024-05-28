const $hw_page = document.getElementById('HW');
const $hw_page_button_nxt = $hw_page.querySelectorAll('.block-button-next');
const $hw_page_button_prv = $hw_page.querySelectorAll('.block-button-prev');
const $hw_page_radio = $hw_page.querySelectorAll('.radio-button');

/**
 * Объект для хранения данных блока формы
 * @type {{_selected: *[], _count: number, _total: number}}
 */
let hw_page_object = {_selected: [], _count: 0, _total: $hw_page.querySelectorAll('.hw-element').length};
let hw_page_blocks = {};

window.addEventListener('load', function () {
    $hw_page.querySelectorAll('.sub-block').forEach(function (e) {
        hw_page_blocks[e.id] = e;
    })
})

$hw_page_button_nxt.forEach(function (e) {
    e.addEventListener('click', function () {
        move_to_another_block(this.closest('.sub-block').id, 1, hw_page_blocks);
    })
})

$hw_page_button_prv.forEach(function (e) {
    e.addEventListener('click', function () {
        move_to_another_block(this.closest('.sub-block').id, -1, hw_page_blocks);
    })
})

$hw_page_radio.forEach(function (e) {
    e.addEventListener('click', function () {
        if (hw_page_object._selected.indexOf(this.name) === -1){
            hw_page_object._selected.push(this.name);
            hw_page_object._count++;
            update_button_counter('hw-page', hw_page_object, 'Hardware');
            this.closest('div').style.border = 'none';
        }
    })
})




