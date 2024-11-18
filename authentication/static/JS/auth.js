const passwordToggles = document.querySelectorAll('.password-toggle');
const forms = {
    login: document.getElementById("login-form"),
    registration: document.getElementById("reg")
};

passwordToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
        const input = this.previousElementSibling;
        const icon = this.querySelector('i');

        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    });
});

async function autoLogin(username, password) {
    const formData = new FormData();
    formData.append('login', username);
    formData.append('password', password);

    try {
        const response = await fetch("/auth/", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: formData
        });

        if (response.ok) {
            window.location.href = "/";
        } else {
            showSnackbar("Ошибка автоматического входа");
        }
    } catch (error) {
        showSnackbar("Ошибка при попытке входа");
    }
}

if (forms.registration) {
    const $password = document.getElementById("password");
    const $rePassword = document.getElementById("re-password");
    const $username = document.getElementById("username");
    const $email = document.getElementById("email");

    forms.registration.addEventListener("submit", async (evt) => {
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

        try {
            const response = await fetch("/auth/registration", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
                body: new FormData(forms.registration)
            });

            if (response.ok) {
                await autoLogin($username.value, $password.value);
            } else {
                const text = await response.text();
                showSnackbar(text || "Ошибка при регистрации");
                if (text.includes("уже существует")) {
                    $username.style.borderColor = "red";
                }
            }
        } catch (error) {
            showSnackbar("Произошла ошибка при отправке данных");
        }
    });

    $username.addEventListener("input", () => {
        $username.style.borderColor = "";
    });

    $password.addEventListener("input", () => {
        if ($rePassword.value) {
            validatePasswords($password, $rePassword);
        }
    });

    $rePassword.addEventListener("input", () => {
        validatePasswords($password, $rePassword);
    });
}

if (forms.login) {
    forms.login.addEventListener("submit", async (evt) => {
        evt.preventDefault();
        const formData = new FormData(forms.login);

        try {
            const response = await fetch("/auth/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
                body: formData
            });

            if (response.ok) {
                window.location.href = "/";
            } else {
                const text = await response.text();
                showSnackbar(text || "Ошибка при входе");
            }
        } catch (error) {
            showSnackbar("Произошла ошибка при отправке данных");
        }
    });
}

function validatePasswords(password1, password2) {
    const passwordsMatch = password1.value === password2.value;
    const borderColor = passwordsMatch ? "" : "red";
    password1.style.borderColor = borderColor;
    password2.style.borderColor = borderColor;
}