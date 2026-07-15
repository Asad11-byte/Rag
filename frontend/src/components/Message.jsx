import ReactMarkdown from "react-markdown";

function Message({ role, content }) {

    return (

        <div className={`message ${role}`}>

            <div className="bubble">

                <ReactMarkdown>

                    {content}

                </ReactMarkdown>

            </div>

        </div>

    );

}

export default Message;