document.addEventListener('DOMContentLoaded', function() {
    const tabElements = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabElements.forEach(tabElement => {
        const tab = new bootstrap.Tab(tabElement);

        tabElement.addEventListener('click', event => {
            event.preventDefault();
            tab.show();
            tabElements.forEach(el => el.classList.remove('active'));
            event.currentTarget.classList.add('active');
        });
    });

    const $personalForm = document.getElementById('personal-form');
    if ($personalForm) {
        $personalForm.addEventListener('submit', (evt) => {
            evt.preventDefault();

            fetch('/profile/update-profile/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
                body: new FormData($personalForm)
            })
            .then(response => {
                if (response.ok) {
                    showSnackbar('Профиль успешно обновлен');
                } else {
                    return response.text().then(text => {
                        showSnackbar(text || 'Ошибка при обновлении профиля');
                    });
                }
            })
            .catch(error => {
                showSnackbar('Произошла ошибка при отправке данных');
            });
        });
    }

    const $passwordForm = document.getElementById('password-form');
    if ($passwordForm) {
        $passwordForm.addEventListener('submit', (evt) => {
            evt.preventDefault();

            const newPassword = document.getElementById('new_password').value;
            const confirmPassword = document.getElementById('confirm_password').value;

            if (newPassword !== confirmPassword) {
                showSnackbar('Пароли не совпадают');
                return;
            }

            if (newPassword.length < 8) {
                showSnackbar('Пароль должен содержать минимум 8 символов');
                return;
            }

            fetch('/profile/update-password/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
                body: new FormData($passwordForm)
            })
            .then(response => {
                if (response.ok) {
                    showSnackbar('Пароль успешно изменен');
                    $passwordForm.reset();
                } else {
                    return response.text().then(text => {
                        showSnackbar(text || 'Ошибка при изменении пароля');
                    });
                }
            })
            .catch(error => {
                showSnackbar('Произошла ошибка при отправке данных');
            });
        });
    }
});