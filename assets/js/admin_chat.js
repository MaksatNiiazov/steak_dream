document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('chat-message-input');
    const messageSubmit = document.getElementById('chat-message-submit');
    let ws = null;

    function setupWebSocket(userId) {
        if (ws) {
            ws.close(); // Закрыть существующее соединение перед открытием нового
        }

        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${protocol}${window.location.host}/ws/chat/${userId}/`;
        ws = new WebSocket(wsUrl);

        ws.onopen = () => console.log(`WebSocket connection established for user ${userId}`);
        ws.onerror = error => console.error('WebSocket error:', error);
        ws.onmessage = event => displayMessage(JSON.parse(event.data));
        ws.onclose = () => console.log('WebSocket connection closed');
    }

    function openChat(userId) {
        if (!userId || userId === "null") {
            console.error('Invalid user ID:', userId);
            return;
        }

        setupWebSocket(userId);
        fetch(`/get-user-orders/?user_id=${userId}`)
            .then(response => response.json())
            .then(data => displayOrders(data.orders))
            .catch(error => console.error('Error loading orders:', error));

        chatContainer.style.display = 'block';
    }

    function displayMessage(data) {
        const messageElement = document.createElement('li');
        messageElement.innerHTML = `<strong>${data.sender_username}:</strong> ${data.message}`;
        chatMessages.appendChild(messageElement);
    }

    function displayOrders(orders) {
        const ordersContainer = document.getElementById('orders-container');
        ordersContainer.innerHTML = ''; // Очистить предыдущие заказы
        orders.forEach(order => {
            const orderElement = document.createElement('div');
            orderElement.textContent = `Order #${order.id}: Status - ${order.status}`;
            ordersContainer.appendChild(orderElement);
        });
    }

    document.querySelectorAll('.user-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const userId = this.dataset.userId;
            openChat(userId);
        });
    });

    messageSubmit.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message && ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ message }));
            messageInput.value = '';
        }
    });
});
