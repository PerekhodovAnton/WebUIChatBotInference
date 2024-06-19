import React, { useState, useEffect } from 'react';
import './ChatBot.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faRobot } from '@fortawesome/free-solid-svg-icons'; // Import the icons you want to use

function ChatBot() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [botTyping, setBotTyping] = useState(false);

    const handleUserMessage = async (text) => {
        const userMessage = { text, sender: 'user' };
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setBotTyping(true);

        try {
            const response = await fetch('http://0.0.0.0:8001/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                throw new Error('Error sending request to the model');
            }

      const data = await response.json();
      const botMessage = { text: '', sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botMessage]);
      await typeMessage(data.message, botMessage); // Печать сообщения по буквам
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  const typeMessage = async (text, message) => {
    for (let i = 0; i < text.length; i++) {
      await delay(20); // Задержка между выводом каждой буквы (в миллисекундах)
      message.text += text[i];
      setMessages(prevMessages => [...prevMessages]);
    }
  };

  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    const handleMessageSubmit = (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;
        handleUserMessage(inputValue);
        setInputValue('');
    };

    useEffect(() => {
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="chat-container">
            <div id="chat-window" className="chat-window">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender}`}>
                        <span className="message-sender">
                            {message.sender === 'user' ? 
                                <FontAwesomeIcon icon={faUser} className="icon" /> :
                                <FontAwesomeIcon icon={faRobot} className="icon" />
                            }
                        </span>
                        {message.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleMessageSubmit} className="message-form">
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
}

export default ChatBot;
