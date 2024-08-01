const $links = document.querySelector(".links");
const $expand_link_list_button = document.getElementById("links__expand-button");

const $hw_button = document.getElementById("hw_block");
const $sw_button = document.getElementById("sw_block");
const $pr_button = document.getElementById("pr_block");

const $hw_block = document.getElementById("hw");
const $hw_links = document.querySelectorAll(".hw")

$expand_link_list_button.addEventListener("click", ()=>{
    $links.classList.toggle("links--expanded");
    $links.classList.toggle("links--collapsed");
});

$hw_button.addEventListener("click", ()=>{
    $hw_block.classList.toggle("hidden");
    $hw_links.forEach(el => {
        el.classList.toggle("hidden")
    })
})