const $table_rows = document.querySelectorAll("table > tbody > tr");
const $review_modal = document.getElementById("review");
const $review_modal_data = document.getElementById("review-data");
const $delete_button = document.getElementById("delete");

let current_id = null
let current_row = null

$table_rows.forEach(function (el) {
    el.addEventListener("click", function(evt){
        current_row = evt.target.parentElement
        current_id = current_row.querySelectorAll("td")[0].textContent;

        fetch("/employee-evaluation/review?"+ new URLSearchParams({"id": current_id}),
            {method: "GET"}).then(resp => {
                resp.text().then(msg => {
                   $review_modal_data.innerHTML = JSON.parse(msg).data;
                   $review_modal.showModal();
                });
        });
    });
});

$delete_button.addEventListener("click", ()=>{
    fetch(`/employee-evaluation/delete-review/${current_id}`, {
        method: "DELETE",
        headers:{"X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value},
    }).then(resp => {
        if (!resp.ok){
            resp.text().then((msg) => {
                showSnackbar(msg);
            });
        } else {
            showSnackbar("Ревью удалено!");
            current_row.remove();
            $modal.close();
        }
    });
});