// let active_tab = "#HW";
//
// $hw_element = $(".hw-element");
// $sw_element = $(".sw-element");
// $skills_element = $(".processes-element");
// $error_box = $("#error-box");
//
// $hw_page_button = $("#HW-page");
// $sw_page_button = $("#SW-page");
// $skills_page_button = $("#skills-page");
// $finish_button = $("#finish");
//
// hw_object = {_count: 0, _total: $hw_element.toArray().length, _selected: [], _id: "HW"};
// sw_object = {_count: 0, _total: $sw_element.toArray().length, _selected: [], _id: "SW"};
// skills_object = {_count: 0, _total: $skills_element.toArray().length, _selected: [], _id: "Processes"};
//
//
// $("#start").on('click',function() {
//     if (RegExp("^[А-ЯЁ][а-яё]+\\s[А-ЯЁ][а-яё]*").exec($("#user_name_input").val()) === null){
//         void show_warning("Только Фамилия и Имя, только Кириллица, Слова с заглавной буквы")
//     }
//     else {
//         $('#user_name').css("display", "none");
//         $(".form-navigation-button").css("display", "inline-block");
//     }
// });
//
// $hw_page_button.on("click", function () {
//     $(active_tab).css("display", "none");
//     active_tab = "#HW";
//     $("#HW").css("display", "block");
// });
// $sw_page_button.on("click", function () {
//     $(active_tab).css("display", "none");
//     active_tab = "#SW";
//     $("#SW").css("display", "block");
// });
// $skills_page_button.on("click", function () {
//     $(active_tab).css("display", "none");
//     active_tab = "#Processes";
//     $("#Processes").css("display", "block");
// });
//
// $finish_button.on("click", function () {
//     // if (hw_object._count === hw_object._total && sw_object._count === sw_object._total && skills_object._count === skills_object._total){
//     if (true){
//         console.log(JSON.stringify($("#self-assessment-form").serializeArray()))
//          $.ajax({
//         url: '/upload-assessment',
//         type: "POST",
//         headers: {
//             'Accept': 'application/text',
//             'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
//         },
//         data: {user_data: JSON.stringify($("#self-assessment-form").serializeArray()),
//         csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
//         dataType: "json",
//         success(msg){
//             console.log(msg);
//         },
//         error(msg){
//             console.log(msg)
//         }
//     });
//     }
//     else{
//         void show_warning("Сначала завершите самооценку")
//     }
// })
//
// $hw_element.on("change", function () {
//     console.log("changed")
//     update_counter(this, hw_object, $hw_page_button);
// })
//
// $sw_element.on("change", function () {
//     update_counter(this, sw_object, $sw_page_button);
// })
//
// $skills_element.on("change", function () {
//     update_counter(this, skills_object, $skills_page_button);
// })
//
// async function show_warning(text) {
//     $error_box.text(text);
//     $error_box.fadeTo("slow", 1);
//     await new Promise(r => setTimeout(r, 5000));
//     $error_box.fadeTo("slow", 0);
//     await new Promise(r => setTimeout(r, 1000));
//     $error_box.css("display", "none")
// }
// function update_counter(element, object, button_object){
//
// }
