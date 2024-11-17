document.addEventListener('DOMContentLoaded', function() {
    const uploadButton = document.getElementById('upload-certificate');
    const certificateModal = new bootstrap.Modal(document.getElementById('certificateModal'));
    const certificateForm = document.getElementById('certificate-form');

    uploadButton.addEventListener('click', () => {
        certificateModal.show();
    });

    certificateForm.addEventListener('submit', function(e) {
        e.preventDefault();

        fetch('/certificate/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new FormData(this)
        })
        .then(response => {
            if (response.ok) {
                showSnackbar('Сертификат успешно загружен');
                certificateModal.hide();
                location.reload();
            } else {
                return response.text().then(text => {
                    showSnackbar(text || 'Ошибка при загрузке сертификата');
                });
            }
        })
        .catch(error => {
            showSnackbar('Произошла ошибка при отправке данных');
        });
    });
});