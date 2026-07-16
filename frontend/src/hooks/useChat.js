import { useState } from "react";

import {
    streamMessage,
} from "../services/api";

export default function useChat() {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    async function send(question) {

        if (!question.trim()) return;

        // Add user message and placeholder assistant message
        setMessages(prev => [
            ...prev,
            {
                role: "user",
                content: question,
            },
            {
                role: "assistant",
                content: "",
                citations: [],
            },
        ]);

        setLoading(true);

        let answer = "";

        // Stream the answer and receive citations afterwards
        const citations = await streamMessage(
            question,
            (chunk) => {

                answer += chunk;

                setMessages(prev => {

                    const updated = [...prev];

                    updated[updated.length - 1] = {
                        role: "assistant",
                        content: answer,
                        citations: [],
                    };

                    return updated;

                });

            }
        );

        // After streaming finishes, attach citations
        setMessages(prev => {

            const updated = [...prev];

            updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                citations: citations || [],
            };

            return updated;

        });

        setLoading(false);
    }

    return {

        messages,

        loading,

        send,

    };

}