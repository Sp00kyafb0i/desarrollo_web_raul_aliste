function zoom(element) {
    element.style.width = "800px";
    element.style.height = "600px";
    document.getElementById(element.name).style.display = "block";
}

function noZoom(element) {
    document.getElementById(element.name).style.width = "320px";
    document.getElementById(element.name).style.height = "240px";
    element.style.display = "none";
}