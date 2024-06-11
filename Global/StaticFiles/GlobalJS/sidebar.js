const $dark_theme = document.getElementById("dark-theme-icon");
const $light_theme = document.getElementById("light-theme-icon");
const $theme_block = document.getElementById("theme");

if (localStorage.getItem("ThemeSKA") === null){
    if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        localStorage.setItem("ThemeSKA", "dark-mode");
        swipe_theme("_", "dark-mode")
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

$dark_theme.addEventListener("click", ()=>{
    swipe_theme("dark-mode", "light-mode");
});

$light_theme.addEventListener("click", ()=>{
    swipe_theme("light-mode", "dark-mode");
});


/**
 * Меняет тему добавляя\удаляя классы и обновляет значение в localStorage
 * @param {string}from
 * @param {string}to
 */
function swipe_theme(from, to) {
    console.log("swiping")
    document.body.classList.remove(from);
    document.body.classList.add(to);
    $theme_block.classList.remove(from);
    $theme_block.classList.add(to);
    localStorage.setItem("ThemeSKA", to);
}