function formSubmit(event) {
    text = document.getElementById("name").value;
    if (text != "Name") {
        document.getElementById("output-box").innerHTML = "Write \"Name\" in the box!";    
        event.preventDefault();    
    }
}

window.onload = function(e){ 
    console.log("Javascript has been loaded");
    document.getElementById("form").addEventListener('submit', formSubmit);
}