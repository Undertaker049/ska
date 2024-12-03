document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('id_role');
    const departmentField = document.getElementById('id_department').closest('.form-row');
    const subordinateField = document.getElementById('id_subordinate_of').closest('.form-row');

    // Валидация доступных для заполнения полей в зависимости от выбранной роли
    function updateFields() {
        const selectedRole = roleSelect.value;

        if (selectedRole === 'admin') {
            departmentField.style.display = 'none';
            subordinateField.style.display = 'none';
            document.getElementById('id_department').value = '';
            document.getElementById('id_subordinate_of').value = '';
        }

        else if (selectedRole === 'supervisor') {
            departmentField.style.display = 'block';
            subordinateField.style.display = 'none';
            document.getElementById('id_subordinate_of').value = '';
        }

        else {
            departmentField.style.display = 'block';
            subordinateField.style.display = 'block';
        }
    }

    // Обработчик изменения значения поля role
    roleSelect.addEventListener('change', updateFields);

    // Вызов функции при загрузке страницы
    updateFields();
});