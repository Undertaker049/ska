let tabs = ["#HW", "#SW", "skills"]
let active_tab = "#HW";
let active_element_class = ".hw-element"
let active_element_number = 0

$("#start").on('click',function() {
    $('#user_name').css('display','none')
    $(active_tab).css("display", "block")
    $("#"+$(active_element_class).toArray()[active_element_number].id).css("display", "block")
    $(".form-button").css("display", "block")
});

$("#form-next").on('click', function () {
    let len = $(active_element_class).toArray().length
    if (len !== active_element_number){
         $("#"+$(active_element_class).toArray()[active_element_number].id).css("display", "none")
         $("#"+$(active_element_class).toArray()[active_element_number+1].id).css("display", "block")
        active_element_number++
    }
})