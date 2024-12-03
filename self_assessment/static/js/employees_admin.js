document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('id_role');
    const departmentField = document.getElementById('id_department');
    const subordinateField = document.getElementById('id_subordinate_of');

    function updateFields() {
        const selectedRole = roleSelect.value;
        const departmentRow = departmentField?.closest('.form-row');
        const subordinateRow = subordinateField?.closest('.form-row');

        if (departmentRow) {

            if (selectedRole === 'admin') {
                departmentRow.style.display = 'none';
                departmentField.value = '';
                departmentField.required = false;
            }

            else {
                departmentRow.style.display = '';
                departmentField.required = true;

                if (!departmentField.closest('form')) {
                    departmentRow.appendChild(departmentField);
                }
            }
        }

        if (subordinateRow) {

            if (selectedRole === 'employee') {
                subordinateRow.style.display = '';
                subordinateField.required = true;

                if (!subordinateField.closest('form')) {
                    subordinateRow.appendChild(subordinateField);
                }
            }

            else {
                subordinateRow.style.display = 'none';
                subordinateField.value = '';
                subordinateField.required = false;
            }
        }
    }

    if (roleSelect) {
        roleSelect.addEventListener('change', updateFields);

        // Вызываем функцию при загрузке страницы
        updateFields();
    }
});