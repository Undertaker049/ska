const $category = document.getElementById("category");
const $upload_certificate_button = document.getElementById("upload-certificate");
const $close_modal_button = document.getElementById("close-modal");

const $form_modal = document.getElementById("form-modal");
const $form = document.getElementById("certificate-form");

const $table_row = document.querySelectorAll("#certificates > tbody > tr");

const category_data = {
    "BURA": ["Data Protector", "StoreOnce", "(Empty)"],
    "Compute": ["Apollo", "BladeSystem", "Integrity", "ProLiant", "Synergy", "(Empty)"],
    "Hybrid IT": ["CloudSystem", "OneView", "(Empty)"],
    "ITIL": ["ITSM"],
    "Networking": ["ProCurve", "FlexNetwork", "(Empty)"],
    "Operating System": ["HP-UX", "RHEL", "(Empty)"],
    "Software": ["Asset", "BSM", "IDOL", "Insight", "NMM", "OpenView", "Operations", "SDM", "Service Manager", "SiteScope", "uCMDB", "Vertica", "(Empty)"],
    "Storage": ["3PAR", "MSA", "Nimble", "SAN", "StorageWorks", "Tape", "(Empty)"]
};

$category.addEventListener("change", function (){
    let cat = this.value;
    if (document.getElementById("subcategory") === null) {
        document.getElementById("for-sub-cat").innerHTML = "<p><label for='subcategory'>Суб-категория</label><br><select id='subcategory' name='subcategory'></select></p>";
    }
    document.getElementById("subcategory").innerHTML = "";

    let sub_cat = document.getElementById("subcategory");

    let arr = category_data[cat];
    for (let i = 0; i < arr.length; i++) {
        const option = document.createElement('option');
        option.value = arr[i];
        option.textContent = arr[i];
        sub_cat.appendChild(option);
    }
});

$upload_certificate_button.addEventListener("click", ()=>{
    $form_modal.showModal();
});

$close_modal_button.addEventListener("click", ()=>{
    $form_modal.close();
});

$form_modal.addEventListener("close", ()=>{
    $form.reset();
});

$table_row.forEach(function (e) {
    e.addEventListener("click", function (ev) {
        // первый элемент строки таблицы - id, так что можно обойтись querySelector
        location.href = "/certificate/about?id=" + ev.target.parentElement.querySelector("td").textContent;
    });
});