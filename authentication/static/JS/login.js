
document.getElementById("submit").addEventListener("click", ()=>{
        fetch("/auth", {
        method: "POST",
        headers:{"X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value},
        body: new URLSearchParams({login: document.getElementById("login").value, password: document.getElementById("password").value }),
    }).then(resp => {
        if (resp.status === 404){
            resp.text().then((msg) => {
                showSnackbar(msg);
            });
        } else{
            location.href = resp.url;
        }
    });
});