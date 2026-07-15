import { useState } from "react";

import { Send } from "lucide-react";

import "../styles/input.css";

function ChatInput({ onSend }) {

    const [text, setText] = useState("");

    function handleSend() {

        if (!text.trim()) return;

        onSend(text);

        setText("");

    }

    return (

        <div className="chat-input-container">

            <input

                value={text}

                onChange={(e) => setText(e.target.value)}

                onKeyDown={(e) => {

                    if (e.key === "Enter") {

                        handleSend();

                    }

                }}

                placeholder="Ask something..."

            />

            <button onClick={handleSend}>

                <Send size={18} />

            </button>

        </div>

    );

}

export default ChatInput;