const apiUrl = 'https://three-tier-webapp-195183330861.us-central1.run.app/messages';  // Replace with actual URL

function fetchMessages() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(messages => {
            const list = document.getElementById('messageList');
            list.innerHTML = '';
            messages.forEach(msg => {
                const li = document.createElement('li');
                li.textContent = msg.message;
                list.appendChild(li);
            });
        });
}

function addMessage() {
    const message = document.getElementById('messageInput').value;
    fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    }).then(() => {
        document.getElementById('messageInput').value = '';
        fetchMessages();
    });
}

fetchMessages();
