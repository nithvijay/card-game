var socket = io({transports: ['websocket']});
console.log("Room: " + room);
document.getElementById("chatBox").style.display = 'none';
document.getElementById("cardBox").style.display = 'none';
//makes users join the room only when they have made a username
document.getElementById("nameButton").addEventListener('click', function(){
    username = document.getElementById("nameBox").value;
    socket.emit('join', {username: username, room: room});
    document.getElementById("nameSubmission").style.display = 'none';           // Hide
    document.getElementById("chatBox").style.display = 'block';          // Show
    document.getElementById("cardBox").style.display = 'block';          // Show
    document.getElementById("usersname").innerHTML = "Hi " + username
});


// socket.io event handlers
socket.on('connect', function() {
    console.log("Socket is connected");
    socket.on('disconnect', function() {
        console.log("Socket is disconnected");
    });
});

socket.on('debug', function(data){
    document.getElementById("debug").innerHTML = "SID: " + data['sid'] + "<br>" + data['session'] + "<br>" + document.getElementById("debug").innerHTML;
});

socket.on('chat message', function(data) {
    document.getElementById("messagesList").innerHTML = document.getElementById("messagesList").innerHTML + "<br>" + data['message'];
});


socket.on('message_history', function(data){
    for (let i = 0; i < data['message_history'].length; i++) {
        document.getElementById("messagesList").innerHTML = "<br>" + data['message_history'][i] + document.getElementById("messagesList").innerHTML;   
    }
    document.getElementById("messagesList").innerHTML = "Messages:" + document.getElementById("messagesList").innerHTML;
});

socket.on('update_room', function(data){
    table = document.getElementById("userListTable");
    table.innerHTML = "Users in Room";
    for (let i = 0; i < data['room_occupants'].length; i++) {
        table.innerHTML += "<br>" + data['room_occupants'][i];
    }
});




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

document.getElementById("deleteHistory").addEventListener('click', function(){
    socket.emit("delete history", {room: room});
});

array = document.getElementsByClassName("grid-item");
for (let i = 0; i < array.length; i++) {
    array[i].addEventListener("mouseenter", function(){
        array[i].style.background = 'yellow'
    });
    array[i].addEventListener("mouseleave", function(){
        array[i].style.background = 'white'
    });
}

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