import { useRef, useState } from "react";
import { Upload } from "lucide-react";

import { uploadPDF } from "../services/api";

function UploadButton() {
    const inputRef = useRef(null);

    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState("");

    async function handleUpload(event) {
        const file = event.target.files[0];

        if (!file) return;

        setUploading(true);
        setStatus("Uploading and indexing PDF...");

        try {
            const response = await uploadPDF(file);

            setStatus(
                response.message ||
                    "✅ PDF uploaded and indexed successfully."
            );
        } catch (error) {
            setStatus(
                error.response?.data?.detail ||
                    "❌ Upload failed."
            );
        } finally {
            setUploading(false);

            event.target.value = "";
        }
    }

    return (
        <div>

            <button
                className="upload-btn"
                disabled={uploading}
                onClick={() => inputRef.current.click()}
            >
                <Upload size={18} />

                {uploading ? "Uploading..." : "Upload PDF"}
            </button>

            <input
                ref={inputRef}
                type="file"
                accept=".pdf"
                hidden
                onChange={handleUpload}
            />

            {status && (
                <p className="upload-status">
                    {status}
                </p>
            )}

        </div>
    );
}

export default UploadButton;