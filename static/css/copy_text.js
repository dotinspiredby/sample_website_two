function copyText(id) {
    var text = document.getElementById(id);
    navigator.clipboard.writeText(text.innerText);
    alert("Copied To Clipboard");
}

