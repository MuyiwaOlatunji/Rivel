// app/static/js/chat.js — Grok AI Chatbot
document.addEventListener("DOMContentLoaded", function () {
  const chatWidget = document.getElementById("chat-widget");
  const chatMessages = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const openButton = document.getElementById("open-chat");
  const closeButton = document.getElementById("close-chat");

  openButton.addEventListener("click", () => chatWidget.classList.remove("hidden"));
  closeButton.addEventListener("click", () => chatWidget.classList.add("hidden"));

  chatInput.addEventListener("keypress", function(e) {
    if (e.key === 'Enter') {
      const message = this.value.trim();
      if (message) {
        chatMessages.innerHTML += `<p class="text-blue-600 mt-2"><strong>You:</strong> ${message}</p>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        this.value = '';

        fetch('/api/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({query: message})
        })
        .then(res => res.json())
        .then(data => {
          chatMessages.innerHTML += `<p class="text-green-600 mt-2"><strong>RIVEL AI:</strong> ${data.response}</p>`;
          chatMessages.scrollTop = chatMessages.scrollHeight;
        });
      }
    }
  });

  // Welcome message
  chatMessages.innerHTML += `<p class="text-gray-600">Hi! I'm RIVEL AI. How can I help you today? Ask about products, shipping, or recommendations!</p>`;
});