const $form = document.getElementById("reg");
const $password = document.getElementById("password");
const $re_password = document.getElementById("re-password");


/**
 * Функция проверяет что пароли на соответствие при регистрации
 */
$form.addEventListener("submit", (evt)=>{
    if ($password.textContent !== $re_password.textContent){
        showSnackbar("Пароли не совпадают!");
        evt.preventDefault();
    }
});