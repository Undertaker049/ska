// Для теста окна с комментом
// <h1>This is header</h1>
// <strong>Under this header is bold text</strong>
// <ul>
//     <li>And this</li>
//     <li>is</li>
//     <li>list</li>
// </ul>

const $modal = document.getElementById("dialog-modal");
const $modal_edit = document.getElementById("dialog-edit");
const $modal_preview = document.getElementById("dialog-preview");
const $modal_input = document.getElementById("dialog-edit--message");
const $modal_input_preview = document.getElementById("dialog-preview--preview");

const $add_comment_button = document.querySelectorAll(".add-comment");
const $modal_show_preview_button = document.getElementById("dialog-edit--preview");
const $modal_edit_text_button = document.getElementById("dialog-preview--edit")

$add_comment_button.forEach(function (e) {
    e.addEventListener("click", () => {
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

$modal_edit_text_button.addEventListener("click", () => {
    $modal_edit.style.display = "block";
    $modal_preview.style.display = "none";
});
