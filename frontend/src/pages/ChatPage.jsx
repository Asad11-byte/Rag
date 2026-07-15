import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import useChat from "../hooks/useChat";

function ChatPage() {

    const {

        messages,

        send,

    } = useChat();

    return (

        <div className="app">

            <Sidebar />

            <main className="main-content">

                <Header />

                <ChatWindow
                    messages={messages}
                />

                <ChatInput
                    onSend={send}
                />

            </main>

        </div>

    );

}

export default ChatPage;