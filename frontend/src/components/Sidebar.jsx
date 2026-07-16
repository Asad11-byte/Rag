import { FolderOpen, Shield } from "lucide-react";
import { useEffect, useState } from "react";

import UploadButton from "./UploadButton";

import "../styles/sidebar.css";

function Sidebar() {

    const [documents, setDocuments] = useState([]);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_API_URL}/documents`)
            .then((res) => res.json())
            .then((data) => setDocuments(data))
            .catch((err) => console.error(err));
    }, []);

    return (

        <aside className="sidebar">

            <div className="sidebar-header">

                <div className="logo">

                    <Shield size={28} />

                    <h2>AI Research RAG</h2>

                </div>

                <UploadButton />

            </div>

            <div className="chat-history">

                <h4>📚 Uploaded Documents</h4>

                {documents.length === 0 ? (

                    <p className="empty-docs">
                        No PDF uploaded yet.
                    </p>

                ) : (

                    documents.map((doc) => (

                        <div
                            key={doc.name}
                            className="document-item"
                            onClick={() =>
                                window.open(
                                    `${import.meta.env.VITE_API_URL}${doc.url}`,
                                    "_blank"
                                )
                            }
                        >

                            <FolderOpen size={18} />

                            <span>{doc.name}</span>

                        </div>

                    ))

                )}

            </div>

            <div className="sidebar-footer">

                <small>
                    📄 {documents.length} Document
                    {documents.length !== 1 ? "s" : ""}
                </small>

            </div>

        </aside>

    );

}

export default Sidebar;