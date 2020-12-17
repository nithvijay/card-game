var socket = io({transports: ['websocket']});
console.log("Room: " + room);

//makes users join the room only when they have made a username
document.getElementById("nameButton").addEventListener('click', function(){
    username = document.getElementById("nameBox").value;
    socket.emit('join', {username: username, room: room});
    document.getElementById("nameSubmission").style.display = 'none';           // Hide
    document.getElementById("messages").style.display = 'block';          // Show
    document.getElementById("usersname").innerHTML = "Hi " + username
});


// socket.io event handlers
socket.on('connect', function() {
    console.log("Socket is connected")
});

socket.on('disconnect', function() {
    console.log("Socket is disconnected");
});

socket.on('chat message', function(event) {
    document.getElementById("messagesList").innerHTML += "<br>" + event['message'];
})


// Code for sending the message to others. Username is attached the message as well.
document.getElementById("sendMessageButton").addEventListener('click', function(){
    text = document.getElementById("messageBox");
    if (text.value.length > 0) {
        username = document.getElementById("nameBox").value;
        socket.emit("chat", {"username": username, "text": text.value, "room": room}); 
        text.value = "";
    }  
    else {
        alert("Please enter something into the textbox before submitting");
    }
});

// Allows users to press enter to submit their message
document.getElementById("messageBox").addEventListener('keyup', function(event){
    if (event.key == "Enter") {
        document.getElementById("sendMessageButton").click();
    }
});


// Code to connect and disconnect from the socket if necessary
// document.getElementById("connectDisconnect").addEventListener('click', function(){
//     button = document.getElementById("connectDisconnect")
//     if (button.innerHTML == "Disconnect") {
//         socket.disconnect();
//         button.innerHTML = "Connect";
//     } else if (button.innerHTML == "Connect") {
//         socket.connect();
//         button.innerHTML = "Disconnect";
//     }
// });