document.addEventListener('DOMContentLoaded', function() {
    // Инициализация компонентов
    const navItems = document.querySelectorAll('input[name="profile-section"]');
    const sections = document.querySelectorAll('.profile-section');
    const toast = new bootstrap.Toast(document.getElementById('notification-toast'));

    /**
     * Показывает уведомление
     * @param {string} message - текст уведомления
     * @param {string} type - тип уведомления (success/error)
     */
    function showNotification(message, type = 'success') {
        const toastEl = document.getElementById('notification-toast');
        toastEl.querySelector('.toast-body').textContent = message;
        toastEl.className = `toast ${type === 'success' ? 'bg-success' : 'bg-danger'} text-white`;
        toast.show();
    }

    /**
     * Показывает выбранную секцию
     * @param {string} sectionId - идентификатор секции
     */
    function showSection(sectionId) {
        sections.forEach(section => {
            section.style.display = 'none';
            section.classList.remove('active');
        });

        const selectedSection = document.getElementById(`${sectionId}-section`);
        if (selectedSection) {
            selectedSection.style.display = 'block';
            setTimeout(() => {
                selectedSection.classList.add('active');
            }, 50);
        }
    }

    // Обработчики событий для навигации
    navItems.forEach(item => {
        item.addEventListener('change', function() {
            showSection(this.value);
        });
    });

    /**
     * Обработка формы личной информации
     */
    const personalForm = document.getElementById('personal-form');
    if (personalForm) {
        personalForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            try {
                const response = await fetch('/profile/update-profile/', {
                    method: 'POST',
                    body: new FormData(this),
                });

                if (response.ok) {
                    showNotification('Профиль успешно обновлен');
                    setTimeout(() => location.reload(), 1500);
                } else {
                    const error = await response.text();
                    showNotification(error || 'Произошла ошибка при обновлении профиля', 'error');
                }
            } catch (error) {
                showNotification('Произошла ошибка при обновлении профиля', 'error');
            }
        });
    }

    /**
     * Обработка формы безопасности
     */
    const securityForm = document.getElementById('security-form');
    if (securityForm) {
        securityForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            try {
                const response = await fetch('/profile/update-password/', {
                    method: 'POST',
                    body: new FormData(this),
                });

                if (response.ok) {
                    showNotification('Пароль успешно изменен');
                    this.reset();
                } else {
                    const error = await response.text();
                    showNotification(error || 'Произошла ошибка при изменении пароля', 'error');
                }
            } catch (error) {
                showNotification('Произошла ошибка при изменении пароля', 'error');
            }
        });
    }
});