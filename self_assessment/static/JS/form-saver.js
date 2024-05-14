// script.js

document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("modal");
    var choice1 = document.getElementById("choice1");
    var choice2 = document.getElementById("choice2");

    // Показываем модальное окно
    modal.classList.add("show");
    document.body.classList.add("modal-open");

    function closeModal() {
        modal.classList.remove("show");
        document.body.classList.remove("modal-open");
    }

    // Обработчики для кнопок
    choice1.addEventListener("click", function() {
        console.log("Выбор 1");
        closeModal();
    });

    choice2.addEventListener("click", function() {
        console.log("Выбор 2");
        closeModal();
    });
});

