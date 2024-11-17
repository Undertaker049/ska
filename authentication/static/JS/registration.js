const $form = document.getElementById("reg");
const $password = document.getElementById("password");
const $rePassword = document.getElementById("re-password");
const $username = document.getElementById("username");
const $email = document.getElementById("email");

$form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    if ($password.value !== $rePassword.value) {
        showSnackbar("Пароли не совпадают!");
        return;
    }

    if ($password.value.length < 8) {
        showSnackbar("Пароль должен содержать минимум 8 символов");
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test($email.value)) {
        showSnackbar("Введите корректный email адрес");
        return;
    }

    if ($username.value.length < 3) {
        showSnackbar("Имя пользователя должно содержать минимум 3 символа");
        return;
    }

    fetch("/auth/registration", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: new FormData($form)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/auth";
        } else {
            return response.text().then(text => {
                showSnackbar(text || "Ошибка при регистрации");

                if (text.includes("уже существует")) {
                    $username.style.borderColor = "red";
                }
            });
        }
    })
    .catch(error => {
        showSnackbar("Произошла ошибка при отправке данных");
    });
});

$username.addEventListener("input", () => {
    $username.style.borderColor = "";
});

$password.addEventListener("input", () => {
    if ($rePassword.value) {
        validatePasswords();
    }
});

$rePassword.addEventListener("input", () => {
    validatePasswords();
});

function validatePasswords() {
    const passwordsMatch = $password.value === $rePassword.value;
    const borderColor = passwordsMatch ? "" : "red";
    $password.style.borderColor = borderColor;
    $rePassword.style.borderColor = borderColor;
}

