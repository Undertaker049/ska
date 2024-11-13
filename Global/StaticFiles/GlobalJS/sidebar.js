// const $dark_theme = document.getElementById("dark-theme-icon");
// const $light_theme = document.getElementById("light-theme-icon");
const $theme = document.getElementById("theme");

if (localStorage.getItem("ThemeSKA") === null){
    if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        localStorage.setItem("ThemeSKA", "dark-mode");
        swipe_theme("_", "dark-mode");
    } else {
        localStorage.setItem("ThemeSKA", "light-mode");
        swipe_theme("_", "light-mode");
    }
} else {
    swipe_theme("_", localStorage.getItem("ThemeSKA"));
}

document.getElementById('toggleBtn').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('expanded');
});

$theme.addEventListener("click", function () {
    if (localStorage.getItem("ThemeSKA") === "dark-mode"){
        swipe_theme("dark-mode", "light-mode");
    } else {
        swipe_theme("light-mode", "dark-mode");
    }
})


/**
 * Меняет тему добавляя\удаляя классы(light-mode | dark-mode) и обновляет значение в localStorage
 * @param {string}from с <...> темы
 * @param {string}to на <...> тему
 */
function swipe_theme(from, to) {
    document.body.classList.remove(from);
    document.body.classList.add(to);
    $theme.classList.remove(from);
    $theme.classList.add(to);
    localStorage.setItem("ThemeSKA", to);
}