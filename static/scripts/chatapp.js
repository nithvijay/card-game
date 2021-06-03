var socket = io({transports: ['websocket']});


console.log("Room: " + room);
// hiding windows on screen until name is entered
document.getElementById("chatBox").style.display = 'none';
document.getElementById("cardBox").style.display = 'none';
document.getElementById("gameWindow").style.display = 'none';
document.getElementById("sid").style.display = 'block';


// hides name box once button is pressed. Unhides other windows. Also adds user to room, server-side
document.getElementById("nameButton").addEventListener('click', function(){
    username = document.getElementById("nameBox").value;
    document.getElementById("nameSubmission").style.display = 'none';           // Hide
    document.getElementById("chatBox").style.display = 'block';          // Show
    document.getElementById("cardBox").style.display = 'none';          // Show
    document.getElementById("gameWindow").style.display = 'block'; // Show
    document.getElementById("usersname").innerHTML = "Hi " + username

    // adds user to room, server-side
    socket.emit('join', {username: username, room: room});
});


// socket.io event handlers; purpose is for debug for now
socket.on('connect', function() {
    console.log("Socket is connected");
    socket.on('disconnect', function() {
        console.log("Socket is disconnected");
    });
    
});

socket.on('sid', function(data){
    document.getElementById("sid").innerHTML = data
});


socket.on('debug', function(data){
    document.getElementById("debug").innerHTML = "SID: " + data['sid'] + "<br>" + data['session'] + "<br>" + document.getElementById("debug").innerHTML;
});


//////////
// Chat //
//////////

// Client-side event handler when server relays chat message
socket.on('chat message', function(data) {
    document.getElementById("messagesList").innerHTML = document.getElementById("messagesList").innerHTML + "<br>" + data['message'];
});

// event handler for chat messages that existed in the room prior to the user joining
socket.on('message_history', function(data){
    for (let i = 0; i < data['message_history'].length; i++) {
        document.getElementById("messagesList").innerHTML = "<br>" + data['message_history'][i] + document.getElementById("messagesList").innerHTML;   
    }
    document.getElementById("messagesList").innerHTML = "Messages:" + document.getElementById("messagesList").innerHTML;
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

// Deletes message history for the room
document.getElementById("deleteHistory").addEventListener('click', function(){
    socket.emit("delete history", {room: room});
});

//////////
// Room //
//////////

socket.on('update_room', function(data){
    table = document.getElementById("userListTable");
    table.innerHTML = "Users in Room";
    for (let i = 0; i < data['room_occupants'].length; i++) {
        table.innerHTML += "<br>" + data['room_occupants'][i];
    }
});

////////////////
// Game Logic //
////////////////


document.getElementById("gameStartButton").addEventListener('click', function(){
    socket.emit("start_game", {room: room, num_cards: 3})
});

socket.on("game_started", function(context){
    document.getElementById("chatBox").style.display = 'none'; // hide other windows
    document.getElementById("cardBox").style.display = 'none';
    document.getElementById("gameStartButton").style.display = 'none'; // hide start button

    gameWindow = document.getElementById("gameWindow");

    var text = document.createTextNode(JSON.stringify(context));
    gameWindow.appendChild(text);
    data = JSON.parse(context.data)
    sid = document.getElementById("sid").innerHTML;
    renderCards(gameWindow, sid, data);
});

function renderCards(gameWindow, sid, data){
    users = Object.keys(data)
    playingField = document.createElement("div");
    playingField.classList.add("playing-container");
    playingField.setAttribute("id", "playingField")
    gameWindow.appendChild(playingField)

    for (let key = 0; key < users.length; key++) {
        userGridContainer = document.createElement("div") // one per user
        userGridContainer.classList.add("grid-container");
        userCards = data[users[key]] // an array of card dictionaries for each user
        
        for (let cardIndex = 0; cardIndex < userCards.length; cardIndex++) {
            if (users[key] == sid){ // the client is the user that controls the cards
                cardElement = renderIndividualOwnCard(userCards[cardIndex]);
                addListeners(cardElement, userCards[cardIndex]);
            }
            else {
                cardElement = renderIndividualOtherCard(userCards[cardIndex]);
            }
            userGridContainer.appendChild(cardElement);
        }
        gameWindow.appendChild(userGridContainer);
    }
}

function renderIndividualOwnCard(data){
    cardElement = document.createElement("div");
    cardElement.classList.add("grid-item");
    cardElement.classList.add("own");
    cardElement.setAttribute('id', data.id)

    cardElement.appendChild(document.createTextNode(data.text));
    cardElement.appendChild(document.createElement('br'));
    cardElement.appendChild(document.createTextNode("Attack: " + data.attack));
    cardElement.appendChild(document.createElement('br'));
    cardElement.appendChild(document.createTextNode("Cost: " + data.cost));
    cardElement.appendChild(document.createElement('br'));
    cardElement.appendChild(document.createTextNode("ID: " + data.id));
    return cardElement;
}

function renderIndividualOtherCard(data){
    cardElement = document.createElement("div");
    cardElement.classList.add("grid-item");
    cardElement.setAttribute('id', data.id)

    cardElement.appendChild(document.createTextNode("Opponent Card"));
    return cardElement;
}

function addListeners(cardElement, cardData){
    // cardElement.addEventListener("mouseenter", (function(element) {
    //     element.style.background = 'yellow';
    // }).bind(null, cardElement) //first argument is for "this"
    // );

    // cardElement.addEventListener("mouseleave", (function(element) {
    //     element.style.background = 'white';
    // }).bind(null, cardElement) //first argument is for "this"
    // );

    cardClick(cardElement, cardData);
}

function cardClick(cardElement, cardData){
    // element = document.getElementById(cardData.id);
    cardElement.addEventListener('click', (function(data){
        socket.emit('play-card', data.id);
        playingField = document.getElementById("playingField");
        document.getElementById(data.id).remove();
        cardElement = renderIndividualOwnCard(data);
        playingField.appendChild(cardElement);
        
    }).bind(null, cardData));
}

socket.on('play-card', function(data){

});



///////////////
// Reference //
///////////////

socket.on('debug', function(data){
    document.getElementById("debug").innerHTML = "SID: " + data['sid'] + "<br>" + data['session'] + "<br>" + document.getElementById("debug").innerHTML;
});

// array = document.getElementsByClassName("grid-item");
// for (let i = 0; i < array.length; i++) {
//     array[i].addEventListener("mouseenter", function(){
//         array[i].style.background = 'yellow'
//     });

//     array[i].addEventListener("click", function(){
//     });

//     array[i].addEventListener("mouseleave", function(){
//         array[i].style.background = 'white'
//     });
// }


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