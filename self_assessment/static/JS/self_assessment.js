let active_tab = "#HW";

$hw_element = $(".hw-element");
$sw_element = $(".sw-element");
$skills_element = $(".skills-element");

$hw_page = $("#HW-page");
$sw_page = $("#SW-page");
$skills_page = $("#skills-page");

hw_object = {_count: 0, _total: $hw_element.toArray().length, _selected: [], _id: "HW"}
sw_object = {_count: 0, _total: $sw_element.toArray().length, _selected: [], _id: "SW"}
skills_object = {_count: 0, _total: $skills_element.toArray().length, _selected: [], _id: "Skills"}



$("#start").on('click',function() {
    $('#user_name').css("display","none");
    $(".form-navigation-button").css("display","inline-block");
});

$hw_page.on("click", function () {
    $(active_tab).css("display", "none");
    active_tab = "#HW";
    $("#HW").css("display", "block");
});
$sw_page.on("click", function () {
    $(active_tab).css("display", "none");
    active_tab = "#SW";
    $("#SW").css("display", "block");
});
$skills_page.on("click", function () {
    $(active_tab).css("display", "none");
    active_tab = "#skills";
    $("#skills").css("display", "block");
});

$hw_element.on("change", function () {
    update_counter(this, hw_object, $hw_page)
})

$sw_element.on("change", function () {
    update_counter(this, sw_object, $sw_page)
})

$skills_element.on("change", function () {
    update_counter(this, skills_object, $skills_page)
})

function update_counter(element, object, button_object){
    let s = `${$(element).closest('div').attr('id')}:${$(element).closest('label').attr('for')}`;
    if ($(element).find(":selected").text() !== "— Select your level —"){
        if (object._selected.indexOf(s) === -1) {
            object._selected.push(s);
            object._count++;
        }
    } else {
        object._selected.splice(object._selected.indexOf(s),1)
        object._count--;
    }
    button_object.text(`${object._id}(${object._count}/${object._total})`);
}
