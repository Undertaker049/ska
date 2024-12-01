import { initializePasswordValidation, initializePasswordToggles } from '/static/js/passwordValidation.js';

const forms = {
    login: document.getElementById("login-form"),
    registration: document.getElementById("reg")
};

// Инициализация переключателей видимости пароля
initializePasswordToggles();

async function autoLogin(username, password) {
    const formData = new FormData();
    formData.append('login', username);
    formData.append('password', password);

    try {
        const response = await fetch("/auth", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: formData
        });

        if (response.ok) {
            window.location.href = "/";
        }

        else {
            showSnackbar("Ошибка автоматического входа");
        }
    }

    catch (error) {
        showSnackbar("Ошибка при попытке входа");
    }
}

if (forms.registration) {
    const $password = document.getElementById("password");
    const $rePassword = document.getElementById("re-password");
    const $username = document.getElementById("username");
    const $email = document.getElementById("email");

    // Инициализация валидации паролей
    const validatePasswords = initializePasswordValidation({
        passwordInput: $password,
        confirmPasswordInput: $rePassword,
        minLength: 8,
        onValidationError: showSnackbar
    });

    forms.registration.addEventListener("submit", async (evt) => {
        evt.preventDefault();

        // Валидация паролей
        if (!validatePasswords()) {
            return;
        }

        // Валидация email
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test($email.value)) {
            showSnackbar("Введите корректный email адрес");
            return;
        }

        // Валидация имени пользователя
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

    // Сброс стиля границы при вводе
    $username.addEventListener("input", () => {
        $username.style.borderColor = "";
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
                const urlParams = new URLSearchParams(window.location.search);
                const nextUrl = urlParams.get('next') || '/';
                window.location.href = nextUrl;
            } else {
                const text = await response.text();
                showSnackbar(text || "Ошибка при входе");
            }
        } catch (error) {
            showSnackbar("Произошла ошибка при отправке данных");
        }
    });
}