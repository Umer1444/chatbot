// Asha Chatbot UI - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatContainer = document.querySelector('.chat-container');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    const cursorEffect = document.querySelector('.cursor-effect');
    const settingsButton = document.querySelector('.settings-btn');
    const colorChartToggle = document.getElementById('color-chart-toggle');
    const settingsPanel = document.querySelector('.settings-panel');
    const clearChatButton = document.getElementById('clear-chat-btn');
    const apiKeyInput = document.getElementById('api-key-input');
    const saveApiKeyButton = document.getElementById('save-api-key-button');
    
    // API Key
    let apiKey = localStorage.getItem('asha_api_key') || '';
    
    // Current API settings
    let currentApiProvider = 'xai'; // Groq API with LLaMA model
    let colorChartEnabled = false;
    let apiFailureCount = 0; // Track consecutive API failures
    
    // Initialize particles
    createParticles();
    
    // Check for saved preferences
    loadUserPreferences();
    
    // Load saved API key to the input field if it exists
    if (apiKeyInput && apiKey) {
        apiKeyInput.value = apiKey;
    }
    
    // Save API Key button
    if (saveApiKeyButton) {
        saveApiKeyButton.addEventListener('click', function() {
            if (apiKeyInput) {
                const newApiKey = apiKeyInput.value.trim();
                if (newApiKey) {
                    apiKey = newApiKey;
                    localStorage.setItem('asha_api_key', apiKey);
                    addMessageToChat('assistant', 'API key has been saved. Your conversations will now use this API key.');
                } else {
                    addMessageToChat('assistant', 'Please enter a valid API key. You can get one from https://console.groq.com');
                }
            }
        });
    }
    
    // Dark mode toggle functionality
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode-active');
            this.classList.toggle('dark-mode-active');
            saveUserPreferences();
        });
    }
    
    // Settings panel toggle
    if (settingsButton) {
        settingsButton.addEventListener('click', function() {
            settingsPanel.classList.toggle('show');
        });
        
        // Close settings when clicking outside
        document.addEventListener('click', function(event) {
            if (!settingsPanel.contains(event.target) && !settingsButton.contains(event.target)) {
                settingsPanel.classList.remove('show');
            }
        });
    }
    
    // Clear chat button
    if (clearChatButton) {
        clearChatButton.addEventListener('click', function() {
            // Clear chat container
            while (chatContainer.firstChild) {
                chatContainer.removeChild(chatContainer.firstChild);
            }
            
            // Clear session on server
            const sessionId = localStorage.getItem('asha_session_id');
            if (sessionId) {
                fetch('/api/clear_session', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        session_id: sessionId
                    })
                }).catch(e => console.error('Error clearing session:', e));
            }
            
            // Add welcome message again
            setTimeout(() => {
                addMessageToChat('assistant', 'Chat cleared. How can I help you today?');
            }, 300);
        });
    }
    
    // Color chart toggle
    if (colorChartToggle) {
        colorChartToggle.addEventListener('change', function() {
            colorChartEnabled = this.checked;
            document.body.classList.toggle('color-chart-enabled', colorChartEnabled);
            saveUserPreferences();
        });
    }
    
    // Custom cursor effect
    if (cursorEffect) {
        document.addEventListener('mousemove', function(e) {
            cursorEffect.style.left = e.clientX + 'px';
            cursorEffect.style.top = e.clientY + 'px';
        });
        
        document.addEventListener('mousedown', function() {
            cursorEffect.classList.add('active');
        });
        
        document.addEventListener('mouseup', function() {
            cursorEffect.classList.remove('active');
        });
    }
    
    // Send message when send button is clicked
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Send message when Enter key is pressed
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }
    
    // Load user preferences
    function loadUserPreferences() {
        try {
            const preferences = JSON.parse(localStorage.getItem('asha_preferences'));
            if (preferences) {
                // Dark mode
                if (preferences.darkMode) {
                    document.body.classList.add('dark-mode-active');
                    if (darkModeToggle) darkModeToggle.classList.add('dark-mode-active');
                }
                
                // Color chart
                colorChartEnabled = preferences.colorChartEnabled || false;
                if (colorChartToggle) colorChartToggle.checked = colorChartEnabled;
                document.body.classList.toggle('color-chart-enabled', colorChartEnabled);
            }
        } catch (e) {
            console.error('Error loading preferences:', e);
        }
    }
    
    // Save user preferences
    function saveUserPreferences() {
        try {
            const preferences = {
                darkMode: document.body.classList.contains('dark-mode-active'),
                colorChartEnabled: colorChartEnabled
            };
            localStorage.setItem('asha_preferences', JSON.stringify(preferences));
        } catch (e) {
            console.error('Error saving preferences:', e);
        }
    }
    
    // Function to create animated particles in the background
    function createParticles() {
        const particles = document.querySelector('.particles');
        if (!particles) return;
        
        const colors = ['#a14dff', '#2e6aff', '#ff3dc9'];
        
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Random properties
            const size = Math.random() * 5 + 1;
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.background = color;
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.animationDuration = `${Math.random() * 10 + 10}s`;
            particle.style.animationDelay = `${Math.random() * 5}s`;
            
            particles.appendChild(particle);
        }
    }
    
    // Function to send message
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Check if API key is set
        if (!apiKey) {
            addMessageToChat('assistant', 'Please set your Groq API key in the settings panel first. You can get one from https://console.groq.com');
            return;
        }
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input field
        messageInput.value = '';
        
        // Apply subtle background effect based on message length
        if (message.length > 50) {
            document.body.classList.add('message-effect-medium');
            setTimeout(() => {
                document.body.classList.remove('message-effect-medium');
            }, 1000);
        } else {
            document.body.classList.add('message-effect-light');
            setTimeout(() => {
                document.body.classList.remove('message-effect-light');
            }, 800);
        }
        
        // Show typing indicator
        showTypingIndicator();
        
        // Get the current session ID from local storage or create one
        let sessionId = localStorage.getItem('asha_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('asha_session_id', sessionId);
        }
        
        // Call the live chat API endpoint
        callLiveChatAPI(message, sessionId);
    }
    
    // Function to add message to chat
    function addMessageToChat(role, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(role === 'user' ? 'user-message' : 'bot-message');
        
        // Check if content length is long enough to be classified as a long message
        if (content.length > 80) {
            messageElement.classList.add('long-message');
        }
        
        // Apply different background colors based on message length for user messages
        if (role === 'user') {
            if (content.length > 100) {
                messageElement.classList.add('very-long-message');
                
                // Add character count display for very long messages
                const countElement = document.createElement('div');
                countElement.classList.add('char-count');
                countElement.textContent = `${content.length} chars`;
                messageElement.appendChild(countElement);
                
            } else if (content.length > 50) {
                messageElement.classList.add('medium-length-message');
                
                // Add subtle character count display for medium messages
                const countElement = document.createElement('div');
                countElement.classList.add('char-count', 'char-count-medium');
                countElement.textContent = `${content.length}`;
                messageElement.appendChild(countElement);
            }
        }
        
        // Create container for the actual message content
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        
        // Check if color chart is enabled and this is a bot message
        if (colorChartEnabled && role === 'assistant') {
            contentElement.innerHTML = formatWithColorChart(content);
        } else {
            // Handle line breaks properly
            contentElement.innerHTML = content.replace(/\n/g, '<br>');
        }
        
        // Add content to the message element
        messageElement.appendChild(contentElement);
        
        chatContainer.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Format message with color chart 
    function formatWithColorChart(content) {
        // Web-friendly colors with their hex values
        const webColors = {
            'red': '#FF5733',
            'green': '#33FF57',
            'blue': '#3357FF',
            'yellow': '#FFFF33',
            'purple': '#9933FF',
            'orange': '#FF9933',
            'pink': '#FF33FF',
            'cyan': '#33FFFF',
            'magenta': '#FF33FF',
            'lime': '#CCFF00',
            'teal': '#008080',
            'indigo': '#4B0082',
            'brown': '#A52A2A',
            'black': '#000000',
            'white': '#FFFFFF',
            'gray': '#808080'
        };
        
        // Replace color words with colored spans
        let formattedContent = content;
        Object.keys(webColors).forEach(color => {
            const regex = new RegExp(`\\b${color}\\b`, 'gi');
            formattedContent = formattedContent.replace(regex, `<span style="color:${webColors[color]}">$&</span>`);
        });
        
        return formattedContent;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingIndicator.appendChild(dot);
        }
        
        // Add thinking text
        const thinking = document.createElement('span');
        thinking.classList.add('thinking');
        thinking.textContent = 'Asha is thinking';
        typingIndicator.appendChild(thinking);
        
        chatContainer.appendChild(typingIndicator);
        scrollToBottom();
    }
    
    // Function to hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to scroll to bottom of chat
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to call the live chat API
    async function callLiveChatAPI(userMessage, sessionId) {
        try {
            // Make API request to our server endpoint
            const response = await fetch('/api/live_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: userMessage,
                    session_id: sessionId,
                    provider: 'xai',
                    api_key: apiKey
                })
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error("API Error Response:", errorText);
                throw new Error(`API responded with status ${response.status}: ${errorText}`);
            }
            
            const data = await response.json();
            console.log("Live Chat API Response:", data);
            
            // Hide typing indicator
            hideTypingIndicator();
            
            // Handle response
            if (data.message) {
                // Add bot response to chat
                addMessageToChat('assistant', data.message);
                
                // Reset API failure count on success
                apiFailureCount = 0;
            } else if (data.error) {
                throw new Error(data.error);
            } else {
                throw new Error('Invalid response format from server');
            }
            
        } catch (error) {
            console.error('Error calling Live Chat API:', error);
            hideTypingIndicator();
            
            // Show error message
            addMessageToChat('assistant', `Error: ${error.message || 'Could not connect to the API'}. Please check your API key and try again.`);
        }
    }
    
    // Progressive Web App support
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/service-worker.js').then(registration => {
                console.log('ServiceWorker registration successful');
            }).catch(error => {
                console.log('ServiceWorker registration failed:', error);
            });
        });
    }
    
    // Add a welcome message
    setTimeout(() => {
        if (!apiKey) {
            addMessageToChat('assistant', 'Welcome to Asha AI! To get started, please set your Groq API key in the settings panel. You can get one from https://console.groq.com');
        } else {
            addMessageToChat('assistant', 'Hello! I\'m Asha, your AI career assistant. I can help with job searches, resume writing, interview preparation, professional development, and mentorship opportunities. How can I assist you today?');
        }
    }, 500);
}); 