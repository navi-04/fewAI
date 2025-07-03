document.addEventListener('DOMContentLoaded', function() {
  const chatOutput = document.getElementById('chat-output');
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const modelSelect = document.getElementById('model-select');
  
  // Add welcome message
  appendMessage('AI', 'Hello! I\'m your AI assistant. How can I help you today?');
  
  // Send message when button is clicked
  sendBtn.addEventListener('click', sendMessage);
  
  // Send message when Enter key is pressed
  userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });
  
  function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Display user message
    appendMessage('User', message);
    
    // Clear input field
    userInput.value = '';
    
    // Show thinking indicator
    const thinkingElement = document.createElement('div');
    thinkingElement.className = 'message ai-message thinking';
    thinkingElement.textContent = 'Thinking...';
    chatOutput.appendChild(thinkingElement);
    
    // Get selected model
    const selectedModel = modelSelect.value;
    
    // Send request to backend
    fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        model: selectedModel
      })
    })
    .then(response => response.json())
    .then(data => {
      // Remove thinking indicator
      chatOutput.removeChild(thinkingElement);
      
      // Display AI response
      appendMessage('AI', data.response);
    })
    .catch(error => {
      console.error('Error:', error);
      // Remove thinking indicator
      chatOutput.removeChild(thinkingElement);
      
      // Display error message
      appendMessage('AI', 'Sorry, I encountered an error. Please try again.');
    });
  }
  
  function appendMessage(sender, text) {
    const messageElement = document.createElement('div');
    messageElement.className = sender === 'User' ? 'message user-message' : 'message ai-message';
    
    const senderElement = document.createElement('strong');
    senderElement.textContent = sender + ': ';
    
    const textElement = document.createElement('span');
    textElement.textContent = text;
    
    messageElement.appendChild(senderElement);
    messageElement.appendChild(textElement);
    
    chatOutput.appendChild(messageElement);
    
    // Scroll to bottom
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }
});