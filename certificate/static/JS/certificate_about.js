const $delete_confirmation_modal = document.getElementById("delete-confirmation-modal");

const $delete_button = document.getElementById("delete");
const $confirm_delete_button = document.getElementById("confirm-delete");
const $cancel_delete_button = document.getElementById("cancel-delete");

$delete_button.addEventListener("click", ()=>{
    console.log("clicked");
    $delete_confirmation_modal.showModal();
});

$confirm_delete_button.addEventListener("click", ()=>{
    $delete_confirmation_modal.close();
    fetch("/certificate/delete", {
        method: "POST",
        headers:{"X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value},
        body: new URLSearchParams({"id": document.getElementById("id").textContent})
    }).then(resp => {
        if (resp.ok){
            showSnackbar("Сертификат удален!");
        }
    });
});

$cancel_delete_button.addEventListener("click", ()=>{
    $delete_confirmation_modal.close();
})



