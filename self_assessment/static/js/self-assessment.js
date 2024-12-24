const assessmentData = {
    HW: { count: 0, total: 0, selections: new Set() },
    SW: { count: 0, total: 0, selections: new Set() },
    Processes: { count: 0, total: 0, selections: new Set() }
};

const modal = new bootstrap.Modal(document.getElementById('restoreModal'));

const blocks = {
    HW: document.getElementById('HW'),
    SW: document.getElementById('SW'),
    Processes: document.getElementById('Processes')
};

const blockButtons = document.querySelectorAll('.block-button');
const finishButton = document.querySelector('.button--finish');

Object.keys(blocks).forEach(blockId => {
    assessmentData[blockId].total = blocks[blockId].querySelectorAll('input[type="radio"][required]').length / 5;
});

blockButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetBlock = button.id.replace('_block', '');

        Object.values(blocks).forEach(block => {
            block.style.display = 'none';
        });

        blockButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        blocks[targetBlock].style.display = 'block';
        button.classList.add('active');
    });
});

document.querySelectorAll('input[type="radio"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const blockId = e.target.closest('.assessment-block').id;
        const inputName = e.target.name;

        if (!assessmentData[blockId].selections.has(inputName)) {
            assessmentData[blockId].count++;
            assessmentData[blockId].selections.add(inputName);
            updateButtonCounter(`${blockId}_block`, assessmentData[blockId]);
        }

        saveFormData();
    });
});

finishButton.addEventListener('click', () => {
    if (isFormComplete()) {
        const formData = collectFormData();
        submitForm(formData);
    } else {
        showSnackbar("Сначала выберите ответ во всех вопросах!", 'warning');
    }
});

document.getElementById('modal__accept').addEventListener('click', () => {
    restoreFormData();
    modal.hide();
});

document.getElementById('modal__decline').addEventListener('click', () => {
    localStorage.removeItem('SKA_DATA');
    modal.hide();
});

function isFormComplete() {
    return Object.values(assessmentData).every(block => block.count === block.total);
}

function collectFormData() {
    return {
        HW: Array.from(assessmentData.HW.selections),
        SW: Array.from(assessmentData.SW.selections),
        Processes: Array.from(assessmentData.Processes.selections)
    };
}

function submitForm(data) {
    fetch(window.urls.self_assessment_upload, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        showSnackbar(data.message || "Результаты записаны!", data.success ? 'success' : 'error');
        if (data.success) {
            finishButton.disabled = true;
            localStorage.removeItem('SKA_DATA');
        }
    })
    .catch(() => {
        showSnackbar("Произошла ошибка при отправке данных", 'error');
    });
}

function updateButtonCounter(buttonId, blockData) {
    const button = document.getElementById(buttonId);
    const blockName = button.textContent.split(' ')[0];
    button.textContent = `${blockName} (${blockData.count}/${blockData.total})`;
}

function saveFormData() {
    localStorage.setItem('SKA_DATA', JSON.stringify(collectFormData()));
}

function restoreFormData() {
    const savedData = JSON.parse(localStorage.getItem('SKA_DATA'));
    if (savedData) {
        Object.entries(savedData).forEach(([blockId, selections]) => {
            selections.forEach(selection => {
                const input = document.querySelector(`#${blockId} input[name="${selection}"]`);
                if (input) {
                    input.checked = true;
                    assessmentData[blockId].selections.add(selection);
                    assessmentData[blockId].count++;
                    updateButtonCounter(`${blockId}_block`, assessmentData[blockId]);
                }
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedData = localStorage.getItem('SKA_DATA');
    if (savedData) {
        modal.show();
    }
});