function showSnackbar(msg) {
    console.log("===========")
    console.log(msg)
    const x = document.getElementById("snackbar");
    x.textContent = msg
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}