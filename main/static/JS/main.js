document.addEventListener('load', function () {
    if (document.getElementById("warning-msg-box").innerText === ""){
        document.getElementById("warning-msg-box").css("display", "none")
    }
    if (document.getElementById("success-msg-box").innerText === ""){
        document.getElementById("success-msg-box").css("display", "none")
    }
})