import ReactMarkdown from "react-markdown";

function Message({
    role,
    content,
    citations = [],
}) {

    return (

        <div className={`message ${role}`}>

            <div className="bubble">

                <ReactMarkdown>
                    {content}
                </ReactMarkdown>

                {role === "assistant" &&
                    citations.length > 0 && (

                        <div className="citations">

                            <h4>📄 Sources</h4>

                            {citations.map((citation, index) => (

                                <div
                                    key={index}
                                    className="citation-item"
                                >
                                    <strong>{citation.source}</strong>

                                    {" — Page "}

                                    {citation.page}

                                    {citation.score && (
                                        <>
                                            {" "}
                                            ({Math.round(
                                                citation.score * 100
                                            )}
                                            %)
                                        </>
                                    )}
                                </div>

                            ))}

                        </div>

                    )}

            </div>

        </div>

    );

}

export default Message;