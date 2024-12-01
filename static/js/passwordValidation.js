export function initializePasswordValidation(options = {}) {

    // Инициализация параметров с значениями по умолчанию
    const {
        passwordInput,
        confirmPasswordInput,
        minLength = 8,
        onValidationError = (message) => {

            if (window.showSnackbar) {
                window.showSnackbar(message);
            }

            else {
                alert(message);
            }
        }
    } = options;

    // Проверка наличия обязательных полей
    if (!passwordInput || !confirmPasswordInput) {
        throw new Error('Password inputs are required');
    }

    const validatePasswords = () => {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // Проверка совпадения паролей
        if (confirmPassword && password !== confirmPassword) {
            onValidationError("Пароли не совпадают");
            return false;
        }

        // Проверка минимальной длины
        if (password.length < minLength) {
            onValidationError(`Пароль должен содержать минимум ${minLength} символов`);
            return false;
        }

        // Сброс стилей при успешной валидации
        passwordInput.style.borderColor = "";
        confirmPasswordInput.style.borderColor = "";
        return true;
    };

    // Обработчик ввода для поля пароля
    passwordInput.addEventListener("input", () => {

        if (confirmPasswordInput.value) {
            validatePasswords();
        }

        passwordInput.style.borderColor = "";
    });

    // Обработчик ввода для поля подтверждения пароля
    confirmPasswordInput.addEventListener("input", () => {
        validatePasswords();

        if (!confirmPasswordInput.value) {
            confirmPasswordInput.style.borderColor = "";
        }
    });

    return validatePasswords;
}

// Инициализация переключателей видимости пароля
export function initializePasswordToggles(container = document) {

    // Поиск всех переключателей видимости пароля в контейнере
    const passwordToggles = container.querySelectorAll('.password-toggle');

    // Добавление обработчиков для каждого переключателя
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            }

            else {
                input.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });
}