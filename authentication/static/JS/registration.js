const $form = document.getElementById("reg");
const $password = document.getElementById("password");
const $re_password = document.getElementById("re-password");

$form.addEventListener("submit", (evt)=>{
    console.log(`${$password} ~ ${$re_password} => ${$password !== $re_password}`)
    if ($password.textContent !== $re_password.textContent){
        showSnackbar("Пароли не совпадают!");
        evt.preventDefault();
    }
})