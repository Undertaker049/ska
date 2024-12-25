/**
 * Инициализация обработчиков для радиокарточек
 */
function initializeRadioCards() {
    const radioCards = document.querySelectorAll('.radio-card');

    radioCards.forEach(card => {
        const input = card.querySelector('input[type="radio"]');

        // Изменение типа input на checkbox для множественного выбора
        input.type = 'checkbox';

        // Обработчик клика по карточке
        card.addEventListener('click', function(e) {

            if (e.target.closest('.custom-tooltip')) {
                return;
            }

            const input = this.querySelector('input');
            input.checked = !input.checked;

            // Вызов события изменения для фильтрации
            input.dispatchEvent(new Event('change'));

            // Обновление визуального состояние карточки
            updateCardState(card, input.checked);
        });

        // Инициализация начального состояния
        updateCardState(card, input.checked);
    });

    // Инициализация поиска в аккордеонах
    initializeAccordionSearch();
}

/**
 * Обновление визуального состояния карточки
 * @param {HTMLElement} card - Элемент карточки
 * @param {boolean} isChecked - Состояние чекбокса
 */
function updateCardState(card, isChecked) {

    if (isChecked) {
        card.classList.add('selected');
    }

    else {
        card.classList.remove('selected');
    }
}

/**
 * Инициализация поиска в аккордеонах
 */
function initializeAccordionSearch() {
    const searchInputs = document.querySelectorAll('.search-box input[data-search-category]');

    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const category = this.dataset.searchCategory;
            const searchValue = this.value.toLowerCase().trim();

            document.querySelectorAll(`input[data-category="${category}"]`).forEach(input => {
                const card = input.closest('.tooltip-wrapper');
                const skillName = input.value.toLowerCase();

                if (searchValue === '' || skillName.includes(searchValue)) {
                    card.style.display = '';
                }

                else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', initializeRadioCards);