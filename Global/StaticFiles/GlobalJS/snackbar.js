/** Метод для отображения сообщения в снэкбаре
 *
 * @param msg Сообщение
 */
function showSnackbar(msg) {
    const x = document.getElementById("snackbar");
    x.textContent = msg
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}