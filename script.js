async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value;
    if (!message.trim()) return;

    appendMessage("You", message);
    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    appendMessage("RamBot 🐏", data.reply);
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>${sender}:</strong> ${message}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
