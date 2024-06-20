const url = new URL(window.location.href);
const id = new URLSearchParams(url.search).get('id');

const $expand_hw_button = document.getElementById("expand-hw");
const $expand_sw_button = document.getElementById("expand-sw");
const $expand_pr_button = document.getElementById("expand-pr");
const $collapse_block_button = document.getElementById("collapse-block");

const $preview = document.getElementById("content-wrapper");
const $hw_block = document.getElementById("hw");
const $sw_block = document.getElementById("sw");
const $pr_block = document.getElementById("pr");


$expand_hw_button.addEventListener("click", ()=>{
    fetch_block("hw", $hw_block);
});
$expand_sw_button.addEventListener("click", ()=>{
    fetch_block("sw", $sw_block);
});
$expand_pr_button.addEventListener("click", ()=>{
    fetch_block("pr", $pr_block);
});

function fetch_block(block_name, block_object){
    location.href = "/employee-evaluation/about-block?"+ new URLSearchParams({'block': block_name, 'id': id});
}