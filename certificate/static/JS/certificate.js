const $category = document.getElementById("category");

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

$category.addEventListener("change", function () {
    let cat = this.value;
    if ((cat === "Generic" || cat === "Support")){
        document.getElementById("for-sub-cat").innerHTML = "";
    }else {
        if (document.getElementById("subcategory") === null) {
            document.getElementById("for-sub-cat").innerHTML = "<p><label for='subcategory'>Суб-категория</label><select id='subcategory' name='subcategory'></select></p>";
        }
        document.getElementById("subcategory").innerHTML = ""

        let sub_cat = document.getElementById("subcategory");

        let arr = category_data[cat]
        for (let i = 0; i < arr.length; i++) {
            const option = document.createElement('option');
            option.value = arr[i];
            option.textContent = arr[i];
            sub_cat.appendChild(option);
        }

    }

});

// function form_data() {
//     let data = {}
//
//     let arr = document.querySelectorAll("input");
//     let element = NaN;
//     for (let i = 0; i < arr.length; i++) {
//         element = arr[i];
//         if (element.type === "file"){
//             const selectedFile = document.getElementById("file").files[0];
//             console.log(selectedFile)
//
//         } else{
//             data[element.name] = element.value
//         }
//
//     }
//
//     return data
// }

// $form.addEventListener("submit", function (event) {
//     event.preventDefault();
//
//     let data = new FormData(event.target)
//     fetch('/certificate', {
//             method: "POST",
//             headers: {
//                 // 'Accept': 'application/text',
//                 // 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
//                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
//                 'Content-Type': 'multipart/form-data'
//             },
//             body:
//                 // csrfmiddlewaretoken: document.querySelector('input[name="csrfmiddlewaretoken"]').value,
//                 data
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