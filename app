import { useState } from 'react';
import './App.css';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';

function App() {
  const [messages, setMessages] = useState([
    {
      message: "Hello, I'm your assistant! Ask me anything by sending an audio message!",
      sentTime: "just now",
      sender: "Assistant"
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (audioFile) => {
    const newMessage = {
      message: "Audio file sent",
      direction: 'outgoing',
      sender: "user"
    };

    const newMessages = [...messages, newMessage];
    setMessages(newMessages);

    setIsTyping(true);

    // Send the audio file to the backend
    const formData = new FormData();
    formData.append('audio', audioFile);

    await fetch("http://localhost:5000/api/chat", { // Replace with your backend URL
      method: "POST",
      body: formData
    })
    .then((response) => response.blob())
    .then((blob) => {
      // Create a URL for the received audio blob and play it
      const audioURL = window.URL.createObjectURL(blob);
      const audio = new Audio(audioURL);
      audio.play();

      // Add the message to the chat
      setMessages([...newMessages, {
        message: "Received audio response",
        sender: "Assistant"
      }]);
      setIsTyping(false);
    })
    .catch((error) => {
      console.error("Error:", error);
      setIsTyping(false);
    });
  };

  const handleFileInput = (e) => {
    const audioFile = e.target.files[0];
    if (audioFile) {
      handleSend(audioFile);
    }
  };

  return (
    <div className="App">
      <div style={{ position: "relative", height: "800px", width: "700px" }}>
        <MainContainer>
          <ChatContainer>       
            <MessageList 
              scrollBehavior="smooth" 
              typingIndicator={isTyping ? <TypingIndicator content="Assistant is processing your audio..." /> : null}
            >
              {messages.map((message, i) => (
                <Message key={i} model={message} />
              ))}
            </MessageList>
            <div style={{ marginTop: "10px" }}>
              <label htmlFor="audioInput">Send Audio:</label>
              <input
                type="file"
                id="audioInput"
                accept="audio/*"
                onChange={handleFileInput}
              />
            </div>
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
}

export default App;
