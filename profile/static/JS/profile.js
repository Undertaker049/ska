const $navButtons = document.querySelectorAll('.nav-button');
const $sections = document.querySelectorAll('.section');
const $personalForm = document.getElementById('personal-form');
const $passwordForm = document.getElementById('password-form');

$navButtons.forEach(button => {
    button.addEventListener('click', () => {
        const target = button.dataset.target;

        $navButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        $sections.forEach(section => {
            section.classList.remove('active');
            if (section.id === target) {
                section.classList.add('active');
            }
        });
    });
});

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
//        console.error('Error:', error);
        showSnackbar('Произошла ошибка при отправке данных');
    });
});

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

    fetch('/profile/update-password/', {  // Изменен URL
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
//        console.error('Error:', error);
        showSnackbar('Произошла ошибка при отправке данных');
    });
});
