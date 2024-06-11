const $form = document.getElementById("reg");
const  $password = document.getElementById("password");
const $re_password = document.getElementById("re-password");

$form.addEventListener("submit", (evt)=>{
    if ($password !== $re_password){
        showSnackbar("Пароли не совпадают!");
        evt.preventDefault();
    }
})