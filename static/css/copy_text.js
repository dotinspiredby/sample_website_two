function copyText(id) {
    var text = document.getElementById(id);
    navigator.clipboard.writeText(text.innerText)
    .then(() => {
        alert("Copied successfully");
      })
      .catch(() => {
        alert("Error");
      });
}

