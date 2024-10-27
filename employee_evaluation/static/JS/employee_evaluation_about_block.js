// Для теста окна с комментом
// <h1>This is header</h1>
// <strong>Under this header is bold text</strong>
// <ul>
//     <li>And this</li>
//     <li>is</li>
//     <li>list</li>
// </ul>
const url = new URL(window.location.href);
const id = new URLSearchParams(url.search).get('id');
const block = new URLSearchParams(url.search).get('block')

const $modal = document.getElementById("dialog-modal");
const $modal_edit = document.getElementById("dialog-edit");
const $modal_preview = document.getElementById("dialog-preview");
const $modal_input = document.getElementById("dialog-edit--message");
const $modal_input_preview = document.getElementById("dialog-preview--preview");
const $nav_menu = document.getElementById("nav-menu");

const $back_button = document.getElementById("back");
const $add_comment_button = document.querySelectorAll(".add-comment");
const $modal_show_preview_button = document.getElementById("dialog-edit--preview");
const $modal_submit_button = document.getElementById("dialog-edit--submit");
const $modal_edit_text_button = document.getElementById("dialog-preview--edit");
const $nav_menu_button = document.getElementById("nav-menu--resize");


let theme = "";

/**
 * Переход обратно к общему обзору на странице сотрудника
 */
$back_button.addEventListener("click", ()=>{
   location.href = `/employee-evaluation/about?id=${id}`;
});

/**
 * @deprecated
 * Описание про блок функций отсюда и до конца файла.
 * Добавить комментарий про дисциплины сотрудника, спорная функция, скорее всего нужно убрать
 */
$add_comment_button.forEach(function (el) {
    el.addEventListener("click", () => {
        theme = el.parentNode.querySelector("h2").textContent
        $modal.showModal();
    });
});

$modal.addEventListener("close", () => {
    $modal_input.value = "";
    $modal_input_preview.innerHTML = "";
});

$modal_show_preview_button.addEventListener("click", () => {
    $modal_edit.style.display = "none";
    $modal_input_preview.innerHTML = $modal_input.value;
    $modal_preview.style.display = "block";

});

$modal_submit_button.addEventListener("click", ()=>{
    let data = {"rev_id": id, "message": $modal_input.value, "block": block, "theme": theme};
    fetch("/employee-evaluation/upload-review", {
        method: "POST",
        headers:{"X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value},
        body: new URLSearchParams(data),
    }).then(resp => {
        if (!resp.ok){
            resp.text().then((msg) => {
                showSnackbar(msg);
            });
        } else{
            showSnackbar("Отзыв записан");
            $modal.close()
        }
    });
});

$modal_edit_text_button.addEventListener("click", () => {
    $modal_edit.style.display = "block";
    $modal_preview.style.display = "none";
});

$nav_menu_button.addEventListener("click", ()=>{
    $nav_menu.classList.toggle("expanded")
})