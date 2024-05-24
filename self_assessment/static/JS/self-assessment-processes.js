const $pr_page = document.getElementById('Processes');
const $pr_page_button_nxt = $pr_page.querySelectorAll('.block-button-next');
const $pr_page_button_prv = $pr_page.querySelectorAll('.block-button-prev');
const $pr_page_radio = $pr_page.querySelectorAll('.processes-radio');

/**
 * Объект для хранения данных блока формы
 * @type {{_selected: *[], _count: number, _total: number}}
 */
let pr_page_object = {_selected: [], _count: 0, _total: $pr_page.querySelectorAll('.processes-radio').length}
let pr_page_blocks = {}

window.addEventListener('load', function () {
    $pr_page.querySelectorAll('.sub-block').forEach(function (e) {
        pr_page_blocks[e.id] = e;
    })
})

$pr_page_button_nxt.forEach(function (e) {
    e.addEventListener('click', function () {
        move_to_another_block(this.closest('.sub-block').id, 1, pr_page_blocks)
    })
})

$pr_page_button_prv.forEach(function (e) {
    e.addEventListener('click', function () {
        move_to_another_block(this.closest('.sub-block').id, -1, pr_page_blocks)
    })
})

$pr_page_radio.forEach(function (e) {
    e.addEventListener('click', function () {
        if (pr_page_object._selected.indexOf(this.name) === -1){
            pr_page_object._selected.push(this.name);
            pr_page_object._count++;
            update_button_counter('processes-page', pr_page_object);
            this.closest('div').style.border = 'none'
        }
    })
})