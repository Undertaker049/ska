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
    const form = document.getElementById("reg");

    // Инициализация валидации паролей
    const validatePasswords = initializePasswordValidation({
        passwordInput: $password,
        confirmPasswordInput: $rePassword,
        minLength: 8,
        onValidationError: (message) => showSnackbar(message, 'error')
    });

    form.addEventListener("submit", async (evt) => {
        evt.preventDefault();

        // Валидация паролей
        if (!validatePasswords()) return;

        // Валидация email
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($email.value)) {
            showSnackbar("Введите корректный email адрес", 'error');
            return;
        }

        // Валидация имени пользователя
        if ($username.value.length < 3) {
            showSnackbar("Имя пользователя должно содержать минимум 3 символа", 'error');
            return;
        }

        const formData = new FormData(form);

        try {
            const response = await fetch("/auth/registration", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new FormData(form)
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.ok) {
                window.location.href = '/';
            } else {
                const text = await response.text();
                showSnackbar(text || "Ошибка при регистрации", 'error');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            showSnackbar("Произошла ошибка при отправке данных", 'error');
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

        try {
            const response = await fetch("/auth", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new FormData(forms.login)
            });

            if (response.ok) {
                const urlParams = new URLSearchParams(window.location.search);
                window.location.href = urlParams.get('next') || '/';
            }

            else {
                const text = await response.text();
                showSnackbar(text || "Ошибка при входе");
            }
        }

        catch (error) {
            showSnackbar("Произошла ошибка при попытке входа");
        }
    });
}