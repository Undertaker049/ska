const $sw_page = document.getElementById('SW');
const $sw_page_button_nxt = $sw_page.querySelectorAll('.block-button-next');
const $sw_page_button_prv = $sw_page.querySelectorAll('.block-button-prev');
const $sw_page_radio = $sw_page.querySelectorAll('.sw-radio');

/**
 * Объект для хранения данных блока формы
 * @type {{_selected: *[], _count: number, _total: number}}
 */
let sw_page_object = {_selected: [], _count: 0, _total: $sw_page.querySelectorAll('.sw-element').length}
let sw_page_blocks = {}

window.addEventListener('load', function () {
    $sw_page.querySelectorAll('.sub-block').forEach(function (e) {
        sw_page_blocks[e.id] = e;
    })
})

$sw_page_button_nxt.forEach(function (e) {
    e.addEventListener('click', function () {
        move_to_another_block(this.closest('.sub-block').id, 1, sw_page_blocks)
    })
})

$sw_page_button_prv.forEach(function (e) {
    e.addEventListener('click', function () {
        move_to_another_block(this.closest('.sub-block').id, -1, sw_page_blocks)
    })
})

$sw_page_radio.forEach(function (e) {
    e.addEventListener('click', function () {
        if (sw_page_object._selected.indexOf(this.name) === -1){
            sw_page_object._selected.push(this.name);
            sw_page_object._count++;
            update_button_counter('sw-page', sw_page_object);
            this.closest('div').style.border = 'none'
        }
    })
})