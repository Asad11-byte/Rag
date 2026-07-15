import { useState } from "react";

import {
    streamMessage,
} from "../services/api";

export default function useChat() {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    async function send(question) {

        if (!question.trim()) return;

        setMessages(prev => [
            ...prev,
            {
                role: "user",
                content: question,
            },
            {
                role: "assistant",
                content: "",
            },
        ]);

        setLoading(true);

        let answer = "";

        await streamMessage(
            question,
            (chunk) => {

                answer += chunk;

                setMessages(prev => {

                    const updated = [...prev];

                    updated[updated.length - 1] = {
                        role: "assistant",
                        content: answer,
                    };

                    return updated;

                });

            }
        );

        setLoading(false);
    }

    return {

        messages,

        loading,

        send,

    };

}