const url = new URL(window.location.href);
const id = new URLSearchParams(url.search).get('id');

const $expand_hw_button = document.getElementById("expand-hw");

const $preview = document.getElementById("content-wrapper")
const $hw_block = document.getElementById("hw")

$expand_hw_button.addEventListener("click", ()=>{
    fetch("/employee-evaluation/about-block?"+ new URLSearchParams({'block': "hw", 'id': id}), {
    }).then(r => {
        if (r.ok){
            r.text().then(msg => {
                msg = JSON.parse(msg)
                console.log(msg)
                $preview.style.display = "none";
                $hw_block.innerHTML = msg.data
            })
        }
    })
});