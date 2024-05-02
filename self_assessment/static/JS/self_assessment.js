let tabs = ["#HW", "#SW", "#skills"];
let tabs_classes = ['.hw-element', '.sw-element', '.skills-element'];
let active_tab = "#HW";
let active_element_class = ".hw-element";
let active_element_number = 0;
let len = 0;

$("#start").on('click',function() {
    $('#user_name').css("display","none");
    $(active_tab).css("display", "block");
    $("#"+$(active_element_class).toArray()[active_element_number].id).css("display", "block");
    $(".form-button").css("display", "block");

    len = $(active_element_class).toArray().length-1;
});

$("#form-next").on('click', function () {
    if (active_element_number+1 <= len) {
        $("#" + $(active_element_class).toArray()[active_element_number].id).css("display", "none");
        $("#" + $(active_element_class).toArray()[active_element_number + 1].id).css("display", "block");
        active_element_number++;
    } else if (tabs.indexOf(active_tab)+1 < tabs.length){
        let index = tabs.indexOf(active_tab)+1

        $(active_tab).css("display", "none");
        $(active_element_class).css("display", "none");

        active_tab = tabs[index]
        active_element_class = tabs_classes[index]
        active_element_number = 0
        len = $(active_element_class).toArray().length-1;

        $(active_tab).css("display", "block");
        $("#"+$(active_element_class).toArray()[active_element_number].id).css("display", "block");
    }
})

$("#form-prev").on('click', function () {
    if (active_element_number-1 >= 0) {
        $("#" + $(active_element_class).toArray()[active_element_number].id).css("display", "none");
        $("#" + $(active_element_class).toArray()[active_element_number - 1].id).css("display", "block");
        active_element_number--;
    } else if (tabs.indexOf(active_tab)-1 >= 0){
        let index = tabs.indexOf(active_tab)-1

        $(active_tab).css("display", "none");
        $(active_element_class).css("display", "none");

        active_tab = tabs[index]
        active_element_class = tabs_classes[index]
        active_element_number = $(active_element_class).toArray().length-1;
        len = active_element_number;

        $(active_tab).css("display", "block");
        $("#"+$(active_element_class).toArray()[active_element_number].id).css("display", "block");
    }
})