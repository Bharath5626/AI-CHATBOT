document.addEventListener('DOMContentLoaded', () => {
  const chatbox = document.getElementById('chatbox');
  const input = document.getElementById('userInput');
  const sendBtn = document.getElementById('sendBtn');

  let isFirstMessage = true;
let conversation = [
  { 
    role: "system", 
    content: "You are a helpful assistant named Talksy. Always answer in clean Markdown format with headings, bullet points, and bold keywords for readability."

  }
];



  function appendMessage(sender, message, type) {
    const div = document.createElement('div');
    div.className = `message ${type}-message`;

    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.textContent = sender === 'user' ? 'U' : 'B';

    const text = document.createElement('div');
    text.className = 'message-text';
    text.innerHTML = marked.parse(message);




    div.appendChild(icon);
    div.appendChild(text);

    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = `
      <div class="message-icon">B</div>
      <div class="message-text">
        <div class="typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
    `;
    chatbox.appendChild(typingDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
  }

  async function sendMessage() {
    const userText = input.value.trim();
    if (!userText) return;

    if (isFirstMessage) {
      chatbox.innerHTML = '';
      chatbox.classList.remove('welcome');
      isFirstMessage = false;
    }

    appendMessage('user', userText, 'user');
    conversation.push({ role: "user", content: userText });

    input.value = '';
    input.disabled = true;
    sendBtn.disabled = true;

    showTypingIndicator();

    try {
      const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer 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'
        },
        body: JSON.stringify({
          model: "llama3-8b-8192",
          messages: conversation,
          max_tokens: 200,
          temperature: 0.7,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      const botReply = data.choices[0].message.content;

      removeTypingIndicator();
      appendMessage('bot', botReply, 'bot');
      conversation.push({ role: "assistant", content: botReply });

    } catch (error) {
      removeTypingIndicator();
      appendMessage('bot', `Error: ${error.message}`, 'bot');
    } finally {
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });
});
