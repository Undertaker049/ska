const $form = document.getElementById("certificate-form")
const $checkbox = document.getElementById("set-to-month");
const $date = document.getElementById("date");
const $category = document.getElementById("category");

const $submit_button = document.getElementById("send");

const category_data = {
    "BURA": ["Data Protector", "StoreOnce", "(Empty)"],
    "Compute": ["Apollo", "BladeSystem", "Integrity", "ProLiant", "Synergy", "(Empty)"],
    "Generic": [""],
    "Hybrid IT": ["CloudSystem", "OneView", "(Empty)"],
    "ITIL": ["ITSM"],
    "Networking": ["ProCurve", "FlexNetwork", "(Empty)"],
    "Operating System": ["HP-UX", "RHEL", "(Empty)"],
    "Software": ["Asset", "BSM", "IDOL", "Insight", "NMM", "OpenView", "Operations", "SDM", "Service Manager", "SiteScope", "uCMDB", "Vertica", "(Empty)"],
    "Storage": ["3PAR", "MSA", "Nimble", "SAN", "StorageWorks", "Tape", "(Empty)"],
    "Support": [""]
};


$checkbox.addEventListener("change", function (){
    if ($checkbox.checked){
        $date.setAttribute("type","month");
    }else {
        $date.setAttribute("type","date");
    }
});

$category.addEventListener("change", function () {
    let cat = this.value;
    if ((cat === "Generic" || cat === "Support")){
        document.getElementById("for-sub-cat").innerHTML = "";
    }else {
        if (document.getElementById("sub-category-p") === null){
            document.getElementById("for-sub-cat").innerHTML = "<p><label for='sub-category'>Суб-категория</label><select id='sub-category' name='sub-category'></select></p>";
        }

        let sub_cat = document.getElementById("sub-category");

        let arr = category_data[cat]
        for (let i = 0; i < arr.length; i++) {
            const option = document.createElement('option');
            option.value = arr[i];
            option.textContent = arr[i];
            sub_cat.appendChild(option);
        }

    }

});

function form_data() {
    let data = {}

    let arr = document.querySelectorAll("input");
    let element = NaN;
    for (let i = 0; i < arr.length; i++) {
        element = arr[i];
        if (element.type === "file"){
            const selectedFile = document.getElementById("file").files[0];
            console.log(selectedFile)

        } else{
            data[element.name] = element.value
        }

    }

    return data
}

// $form.addEventListener("submit", function (event) {
//     event.preventDefault();
//
//     let data =form_data()
//     return false
//     console.log(typeof document.getElementById("file").files[0])
//     fetch('/upload-certificate', {
//             method: "POST",
//             headers: {
//                 // 'Accept': 'application/text',
//                 // 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
//                 'Accept': '*/*',
//                 'Content-Type': 'multipart/form-data'
//             },
//             body: new URLSearchParams({
//                 csrfmiddlewaretoken: document.querySelector('input[name="csrfmiddlewaretoken"]').value,
//                 form: data
//             })
//         })
//         .then(response => {
//             if (!response.ok) {
//                 return response.json().then(err => { console.log(err)});
//             }
//             return response.json();
//         })
//         .catch(err => {
//             console.log(err.text);
//         });
// })