import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

// Upload PDF
export async function uploadPDF(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await API.post("/upload/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
}

// Normal Chat
export async function sendMessage(question) {
    const response = await API.post("/chat/", {
        question,
    });

    return response.data;
}

// Streaming Chat
export async function streamMessage(question, onToken) {

    const response = await fetch(
        `${import.meta.env.VITE_API_URL}/chat/stream`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                question,
            }),
        }
    );

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {

        const { done, value } = await reader.read();

        if (done) break;

        onToken(decoder.decode(value));
    }
}