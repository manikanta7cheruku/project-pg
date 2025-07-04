const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

sendBtn.addEventListener("click", () => {
    const msg = userInput.value.trim();
    if (msg) {
        appendMessage(`🟢 You: ${msg}`);
        fetchResponse(msg);
        userInput.value = "";
    }
});

function appendMessage(text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message");
    msgDiv.textContent = text;
    chatArea.appendChild(msgDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function fetchResponse(topic) {
    appendMessage("⏳ Generating post...");

    fetch("/generate_post", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ topic: topic })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage(`📄 Caption: ${data.caption}`);
        if (data.image_url) {
            appendMessage(`🖼️ Image generated: ${data.image_url}`);
        }
    })
    .catch(() => {
        appendMessage("❌ Error generating post.");
    });
}
