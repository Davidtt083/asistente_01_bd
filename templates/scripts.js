function sendQuestion(question) {
    const loadingIndicatorInterval = showLoadingIndicator();

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `question=${encodeURIComponent(question)}`,
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(loadingIndicatorInterval);
        const chatContainer = document.getElementById('chat');
        const userMessage = document.createElement('div');
        userMessage.className = 'user-message';
        userMessage.textContent = question;
        chatContainer.appendChild(userMessage);

        data.response.forEach(line => {
            const systemMessage = document.createElement('div');
            systemMessage.className = 'system-message';
            systemMessage.textContent = line;
            chatContainer.appendChild(systemMessage);
        });
    })
    .catch(error => {
        clearInterval(loadingIndicatorInterval);
        console.error('Error:', error);
    });
}

document.querySelector('form').addEventListener('submit', event => {
    event.preventDefault();
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();
    if (question) {
        sendQuestion(question);
        questionInput.value = '';
    }
});