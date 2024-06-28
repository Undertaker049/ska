const $table_rows = document.querySelectorAll("table > tbody > tr");
const $review_modal = document.getElementById("review");
const $review_modal_data = document.getElementById("review-data");

$table_rows.forEach(function (el) {
    el.addEventListener("click", function(evt){
        fetch("/employee-evaluation/review?"+ new URLSearchParams({"id": evt.target.parentElement.querySelectorAll("td")[0].textContent}),
            {method: "GET"}).then(resp => {
                resp.text().then(msg => {

                   $review_modal_data.innerHTML = JSON.parse(msg).data;
                   $review_modal.showModal();
                });
        });
    });
});