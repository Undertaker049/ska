const $search_field = document.getElementById("table-search");
const $search_button = document.getElementById("search");
const $table_rows = document.querySelectorAll("table > tbody > tr");

/**
 * Функция для поиска конкретного сотрудника в списке
 */
$search_button.addEventListener("click", ()=>{
    if ($search_field.value !== "") {
        find_rows($search_field.value.split(", "));
    } else {
        $table_rows.forEach(function (el) {
            el.style.visibility = "visible";
        });
    }
});

/**
 * Функция для перехода на страницу с информацией о конкретном сотруднике
 */
$table_rows.forEach(function (el) {
    el.addEventListener("click", function (ev) {
        location.href = `/employee-evaluation/about?id=${ev.target.parentElement.querySelector('td').textContent}`;
    });
});

/**
 * Функция для мягкого поиска строк в таблице. Значения не обязательно должны совпадать полностью.
 * @param {Array[]}q массив строк-параметров запроса
 */
function find_rows(q) {
    if (q.length === 1) {
       q = q[0];
       $table_rows.forEach(function (el) {
           let tds = el.querySelectorAll("td");
           for (let i = 0; i < tds.length; i++) {
               if (tds[i].textContent.includes(q.toString())){
                    el.style.visibility = "visible";
                    return;
               } else {
                   el.style.visibility = "collapse";
               }
           }
       });
   }
   else if (q.length === 2) {
       $table_rows.forEach(function (el) {
           let tds = el.querySelectorAll("td");
           if (tds[0].textContent.includes(q[0].toString()) && tds[1].textContent.includes(q[1].toString())) {
               el.style.visibility = "visible";
           } else {
               el.style.visibility = "collapse";
           }
       })
   }
   else if (q.length > 2) {
       showSnackbar("Максимум аргументов - 2. Прим: 1, Петров");
   }
}