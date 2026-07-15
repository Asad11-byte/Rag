import { useEffect, useRef } from "react";

import Message from "./Message";

import "../styles/chat.css";

function ChatWindow({ messages }) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    if (!messages || messages.length === 0) {
        return (
            <div className="chat-window">
                <div className="welcome">
                    <h1>👋 Welcome</h1>

                    <p>
                        Upload your AI Agent Security PDF and start asking
                        questions about it.
                    </p>

                    <div className="welcome-box">
                        <p>✔ Upload a PDF</p>
                        <p>✔ Ask security questions</p>
                        <p>✔ Get AI-powered answers</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-window">
            {messages.map((message, index) => (
                <Message
                    key={index}
                    role={message.role}
                    content={message.content}
                />
            ))}

            <div ref={bottomRef} />
        </div>
    );
}

export default ChatWindow;