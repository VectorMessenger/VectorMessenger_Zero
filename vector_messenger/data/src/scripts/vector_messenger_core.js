const fetch_interval_ms = 800

$(document).ready(function(){
    $('.scrollbar-macosx').scrollbar();
});

function show_message(message_text) {
    message = document.createElement('p')
    message.className = 'chat-message'
    message.innerText = message_text
    chat_field = document.getElementById("chat-field")
    chat_field.appendChild(message)
}

function fetch_messages() {
    $.get('/fetch_messages', success=show_message)
}

setInterval(fetch_messages, fetch_interval_ms)
