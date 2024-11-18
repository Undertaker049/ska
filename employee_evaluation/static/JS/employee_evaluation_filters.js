const filterForm = document.querySelector('.filters-sidebar');
const employeeCards = document.querySelectorAll('.employee-card');

function applyFilters() {
    const filters = {
        departments: Array.from(document.querySelectorAll('input[name="department"]:checked')).map(cb => cb.value),
        hwSkills: Array.from(document.querySelectorAll('input[name="hw_skill"]:checked')).map(cb => cb.value),
        swSkills: Array.from(document.querySelectorAll('input[name="sw_skill"]:checked')).map(cb => cb.value),
        processes: Array.from(document.querySelectorAll('input[name="process"]:checked')).map(cb => cb.value)
    };

    employeeCards.forEach(card => {
        const shouldShow = checkFilters(card, filters);
        card.style.display = shouldShow ? 'block' : 'none';
    });
}

function checkFilters(card, filters) {
    const cardData = JSON.parse(card.dataset.employee);

    if (filters.departments.length && !filters.departments.includes(cardData.department)) {
        return false;
    }

    if (filters.hwSkills.length && !hasMatchingSkills(cardData.top_skills.hardware, filters.hwSkills)) {
        return false;
    }

    if (filters.swSkills.length && !hasMatchingSkills(cardData.top_skills.software, filters.swSkills)) {
        return false;
    }

    if (filters.processes.length && !hasMatchingSkills(cardData.top_skills.processes, filters.processes)) {
        return false;
    }

    return true;
}

function hasMatchingSkills(cardSkills, filterSkills) {
    return cardSkills.some(skill => filterSkills.includes(skill.name));
}

function resetFilters() {
    filterForm.reset();
    employeeCards.forEach(card => card.style.display = 'block');
}