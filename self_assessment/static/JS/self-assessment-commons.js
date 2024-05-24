/**
 * Автоскролл до следующего блока вопросов
 * @param {string}parent_id ID блока формы (HW, SW etc.)
 * @param {number}shift На сколько блоков сместится вперед(+1) или назад(-1)
 * @param {{_count: number, _total: number}}page_blocks
 */
function move_to_another_block(parent_id, shift, page_blocks) {
            let index = Object.keys(page_blocks).indexOf(parent_id)
        try{
            Object.values(page_blocks)[index+shift].scrollIntoView();
        } catch (err){
            if (!(err instanceof TypeError)){
                let e = new Error(err);
                console.error(e.message)
            }
        }
}

function update_button_counter(button_id, page_object) {
    document.getElementById(button_id).textContent = `HW (${page_object._count}/${page_object._total})`
}