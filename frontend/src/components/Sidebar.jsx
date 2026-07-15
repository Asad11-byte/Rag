import { Plus, Shield } from "lucide-react";

import UploadButton from "./UploadButton";

import "../styles/sidebar.css";

function Sidebar() {

    return (

        <aside className="sidebar">

            <div className="sidebar-header">

                <div className="logo">

                    <Shield size={28} />

                    <h2>AI Security RAG</h2>

                </div>

                <button className="new-chat-btn">

                    <Plus size={18} />

                    New Chat

                </button>

                <UploadButton />

            </div>

            <div className="chat-history">

                <h4>Recent Chats</h4>

            </div>

            <div className="sidebar-footer">

                AI Agent Security RAG

            </div>

        </aside>

    );

}

export default Sidebar;