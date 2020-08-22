const fetch_interval_ms = 800

function show_message(message_text) {
    document.getElementById("chat-field").value = message_text
}

function fetch_messages() {
    $.get('/fetch_messages', success=show_message)
}

setInterval(fetch_messages, fetch_interval_ms)
