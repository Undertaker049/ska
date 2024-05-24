$hw_page_button = document.getElementById('hw-page');
$sw_page_button = document.getElementById('sw-page');
$pr_page_button = document.getElementById('processes-page');
$finish_button = document.getElementById('finish');
$back_button = document.getElementById('back');

$hw_page_button.addEventListener('click', function (){
    hide_form_elements();
    document.getElementById("HW").style.display = 'block';
});

$sw_page_button.addEventListener('click', function () {
    hide_form_elements();
    document.getElementById('SW').style.display = 'block';
})

$pr_page_button.addEventListener('click', function (){
    hide_form_elements();
    document.getElementById("Processes").style.display = 'block';
});

$back_button.addEventListener('click', function () {
    document.querySelector('header').scrollIntoView();
})

function hide_form_elements() {
    document.querySelectorAll('.form-element').forEach(function (e) {
        e.style.display = 'none';
    });
}