const socket = io.connect('http://localhost:5000');

//prompts user for a username
let username = prompt("Enter Username:");

//notifies server of new connection
socket.emit('new_connection', {username:username});

//function to send messages
function sendMessage() {
    const inputElement = document.getElementById('message-input');
    const message = inputElement.value;

    if (message) {
        socket.emit('send_message', { message: message, username:username });
        inputElement.value = '';  // Clear the input field
    }
}

//handle 'user_connected' events
socket.on('user_connected', function(data){
    const chatBox = document.getElementById('chat-box');
    const userElement = document.createElement('p');

    userElement.innerText = '${data.username} has entered the chat.';

    chatBox.appendChild(userElement);
});

//listen for messages from the server
socket.on('receive_message', function(data) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('p');

    messageElement.innerText = '${data.username}: ${data.message}';

    // Append the message to the chat box
    chatBox.appendChild(messageElement);
});





