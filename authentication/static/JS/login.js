document.getElementById('auth-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('login', document.getElementById('login').value);
    formData.append('password', document.getElementById('password').value);

    fetch('/auth/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            const urlParams = new URLSearchParams(window.location.search);
            const nextUrl = urlParams.get('next') || '/';
            window.location.href = nextUrl;
        } else {
            return response.text().then(text => {
                showSnackbar(text || "Ошибка при входе");
            });
        }
    })
    .catch(error => {
        showSnackbar("Произошла ошибка при отправке данных");
    });
});